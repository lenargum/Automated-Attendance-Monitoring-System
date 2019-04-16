import os
from flask import render_template, redirect, url_for, request, jsonify, flash, send_file
from markupsafe import Markup
from app import app
from app.forms import SessionCreateForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app import qrcode
from app import models
from datetime import datetime
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# For faculty: create new session and go to managing page
@app.route("/session/create", methods=['GET', 'POST'])
@login_required
def session_create():
    courses = models.Course.query\
        .join(models.Enrollment)\
        .join(models.User)\
        .join(models.Role)\
        .filter(models.User.id == current_user.id)\
        .filter(models.Role.can_manage_sessions == True).all()
    s_types = models.SessionType.query.all()
    form = SessionCreateForm()
    form.course.choices = [(c.id, c.name) for c in courses]
    form.s_type.choices = [(st.id, st.name) for st in s_types]
    if form.validate_on_submit():
        new_session = models.Session(date=datetime.now(),
                                     faculty_id=current_user.id,
                                     is_closed=False,
                                     type_id=form.s_type.data,
                                     course_id=form.course.data)
        db.session.add(new_session)
        db.session.commit()
        s_id = new_session.id
        return redirect(url_for("session_manage", s_id=s_id))
    return render_template("session_create.html", form=form)


@app.route("/created_sessions")
@login_required
def created_sessions_list():
    if not current_user.is_faculty:
        flash("Only faculty can manage session")
        return redirect("index")
    return render_template("created_sessions_list.html")


@app.route("/attended_sessions", methods=['GET', 'POST'])
@login_required
def attended_sessions_list():
    if request.method == 'GET':
        return render_template("attended_sessions_list.html")
    elif request.method == 'POST':
        if request.form['export_button'] == 'Export to xlsx':
            # formation of xlsx file:
            from xlsxwriter import Workbook
            repository_path = os.path.dirname(os.path.dirname(__file__))

            # workbook init
            workbook = Workbook("temp.xlsx")
            worksheet = workbook.add_worksheet()

            # certain cells formation
            classic_format = workbook.add_format()
            classic_format.set_border()
            classic_date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
            classic_date_format.set_border()
            classic_time_format = workbook.add_format({'num_format': 'HH:mm:ss'})
            classic_time_format.set_border()
            header_format = workbook.add_format({'bold': 1, 'align': 'center'})
            header_format.set_border()
            header_format.set_bottom(2)

            # placing headers on worksheet
            worksheet.write_string(0, 0, "Course", header_format)
            worksheet.set_column('A:A', 20)
            worksheet.write_string(0, 1, "Type", header_format)
            worksheet.set_column('B:B', 12)
            worksheet.write_string(0, 2, "Date", header_format)
            worksheet.set_column('C:C', 15)
            worksheet.write_string(0, 3, "Time", header_format)
            worksheet.write_string(0, 4, "Finished", header_format)

            # placing body of table on worksheet
            current_row = 1
            for session in current_user.sessions:
                worksheet.write_string(current_row, 0, session.course.name, classic_format)
                worksheet.write_string(current_row, 1, session.type.name, classic_format)
                worksheet.write_datetime(current_row, 2, session.date, classic_date_format)
                worksheet.write_datetime(current_row, 3, session.date, classic_time_format)
                worksheet.write_string(current_row, 4, "Yes" if session.is_closed else "No", classic_format)
                current_row += 1

            workbook.close()
            workbook_filename = "{}_{}.xlsx".format(current_user.surname, current_user.name)  # endpoint filename
            return send_file(os.path.join(repository_path, "temp.xlsx"), as_attachment=True,
                             attachment_filename=workbook_filename)


@app.route("/student_sessions/<st_id>")
@login_required
def student_sessions(st_id):
    user = models.User.query.filter_by(id=st_id).first_or_404()
    return render_template("student_sessions.html", user=user)


@app.route("/session/<s_id>")
@login_required
def session_manage(s_id):
    session = models.Session.query\
        .join(models.Course)\
        .join(models.Enrollment)\
        .join(models.User)\
        .join(models.Role)\
        .filter(models.Session.id == s_id)\
        .filter(models.User.id == current_user.id)\
        .filter(models.Role.can_manage_sessions == True).first_or_404()
    return render_template("session.html", session=session)


@app.route("/session_qr/<s_id>")
@login_required
def session_qr(s_id):
    hostname = request.headers["Host"]
    # flash(app.config["SERVER_URL"])
    if hostname.startswith("127.0.0.1") or hostname.startswith("localhost"):
        port = hostname.split(":")[1]
        message = "Accessing from localhost. <a href=http://{}><b>Please use global ip or address instead</b></a>"
        message = message.format(app.config["GLOBAL_IP"] + ":" + port + url_for("session_qr", s_id=s_id))
        flash(Markup(message), "danger")
        # return redirect(url_for("session_qr", s_id=s_id, _external=app.config["SERVER_URL"]+":"+port))
    session = models.Session.query\
        .join(models.Course)\
        .join(models.Enrollment)\
        .join(models.User)\
        .join(models.Role)\
        .filter(models.Session.id == s_id)\
        .filter(models.User.id == current_user.id)\
        .filter(models.Role.can_manage_sessions == True).first_or_404()
    return render_template("session_qr.html", session=session)


# Allow enter and submit attendance data if token is correct
@app.route("/qrcode/<token_key>", methods=['GET', 'POST'])
@login_required
def qr_code_token(token_key):
    token: models.Token = models.Token.query.filter_by(key=token_key).first_or_404()
    if token.expired:
        flash("Sorry! This token is no longer available", "warning")
        return redirect("/index")
    session: models.Session = token.session
    session.students.append(current_user)
    db.session.commit()
    flash("Success! You attendance for {}({}) was recorded".format(session.course.name, session.type.name))
    return redirect("/index")


@app.route('/login', methods=['GET', 'POST'])
def login():
    hostname = request.headers["Host"]
    # flash(app.config["SERVER_URL"])
    if hostname.startswith("127.0.0.1") or hostname.startswith("localhost"):
        port = hostname.split(":")[1]
        message = "Accessing from localhost. <a href=http://{}><b>Please use global ip or address instead</b></a>"
        message = message.format(app.config["GLOBAL_IP"] + ":" + port + url_for("login"))
        flash(Markup(message), "danger")
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Get 'next' argument if exists
        next_page = request.args.get('next')
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            # If 'next' arg exists then append it again
            return redirect(url_for('login', next=next_page))
        login_user(user, remember=form.remember_me.data)
        # If 'next' argument exists and correct then redirect to that page, redirect to 'index' otherwise
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile/<email>')
@login_required
def profile(email):
    user = models.User.query.filter_by(email=email).first_or_404()
    return render_template('profile.html', user=user)


# API calls (to call from client using js and jQuery)

# TODO: only accessible for faculty
@app.route("/api/qr_image")
@login_required
def qrcode_image():
    session_id = request.args.get("session_id", None)
    if not session_id:
        return jsonify({"status": "fail"})
    try:
        session_id = int(session_id)
    except ValueError:
        return jsonify({"status": "fail"})
    token = models.get_token(session_id)
    if not token:
        return jsonify({"status": "fail"})
    key = token.key
    qr_base64 = qrcode(url_for("qr_code_token", token_key=key, _external=True))
    return jsonify({"status": "ok", "image": qr_base64})


# TODO: only accessible for faculty
@app.route("/api/qr_regen")
@login_required
def regen():
    session_id = request.args.get("session_id", None)
    if not session_id:
        return jsonify({"status": "fail"})
    try:
        session_id = int(session_id)
    except ValueError:
        return jsonify({"status": "fail"})
    models.reset_token(session_id)
    return "ok"
