from flask import render_template, redirect, url_for, request, jsonify, flash
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
    # TODO: show only courses that current user can manage
    courses = models.Course.query.all()
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
    return render_template("created_sessions_list.html")


@app.route("/attended_sessions")
@login_required
def attended_sessions_list():
    return render_template("attended_sessions_list.html")


@app.route("/student_sessions/<st_id>")
@login_required
def student_sessions(st_id):
    user = models.User.query.filter_by(id=st_id).first_or_404()
    return render_template("student_sessions.html", user=user)


@app.route("/session/<s_id>")
@login_required
def session_manage(s_id):
    # TODO: restrict only to those who can manage course
    # if not current_user.is_faculty:
    #     flash("Only faculty can manage session")
    #     return redirect("index")
    session = models.Session.query.filter_by(id=s_id).first_or_404()
    return render_template("session.html", session=session)


@app.route("/session_qr/<s_id>")
@login_required
def session_qr(s_id):
    # TODO: restrict only to those who can manage course
    hostname = request.headers["Host"]
    # flash(app.config["SERVER_URL"])
    if hostname.startswith("127.0.0.1"):
        port = hostname.split(":")[1]
        message = "Accessing from localhost. <a href=http://{}><b>Please use global ip or address instead</b></a>"
        message = message.format(app.config["GLOBAL_IP"]+":"+port+url_for("session_qr", s_id=s_id))
        print(message)
        flash(Markup(message), "danger")
        # return redirect(url_for("session_qr", s_id=s_id, _external=app.config["SERVER_URL"]+":"+port))
    session = models.Session.query.filter_by(id=s_id).first_or_404()
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
    flash("Success! You attendance for {} was recorded".format(session.course.name))
    return redirect("/index")


@app.route('/login', methods=['GET', 'POST'])
def login():
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
@login_required
@app.route("/api/qr_image")
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
