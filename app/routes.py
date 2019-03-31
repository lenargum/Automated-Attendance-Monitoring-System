from flask import render_template, redirect, url_for, request, jsonify
from app import app
from app.forms import TokenConfirmForm, SessionCreateForm, LoginForm
from flask_login import current_user, login_user, logout_user
from app import db
from app import qrcode
from app import models
from datetime import datetime


@app.route("/")
@app.route("/index")
def index():
    attendance = models.Attendance.query.all()
    return render_template("index.html", attendance=attendance)


# TODO: only accessible for faculty
@app.route("/session/create", methods=['GET', 'POST'])
def session_create():
    # TODO: take courses relevant to current faculty user
    courses = models.Course.query.all()
    form = SessionCreateForm()
    form.course.choices = [(c.id, c.name) for c in courses]
    if form.validate_on_submit():
        # TODO: use current authorized user
        new_session = models.Session(date=datetime.now(),
                                     faculty_id=1,
                                     course_id=form.course.data)
        db.session.add(new_session)
        db.session.commit()
        s_id = new_session.id
        return redirect(url_for("session_manage", s_id=s_id))
    return render_template("session_create.html", form=form)


# TODO: only accessible for faculty
@app.route("/session/<s_id>")
def session_manage(s_id):
    session = models.Session.query.filter_by(id=s_id).first_or_404()
    return render_template("session.html", session=session)


# TODO: only accessible for faculty
@app.route("/qrcode_generate")
def qr_code_generate():
    return render_template("qrcode_generate.html")


# TODO: only accessible for faculty
@app.route("/qrcode_image")
def qrcode_image():
    token = models.get_token()
    if not token:
        print("fail")
        return jsonify({"status": "fail"})
    key = token.key
    hostname = request.headers["Host"]
    qr_base64 = qrcode(url_for("qr_code_token", token_key=key, _external=hostname))
    return jsonify({"status": "ok", "image": qr_base64})


# TODO: only accessible for faculty
@app.route("/qrcode_regen")
def regen():
    models.reset_token()
    return "ok"


@app.route("/add")
def add_student():
    name = request.args.get('name')
    surname = request.args.get('surname')
    date = request.args.get('date')
    try:
        student = models.Student(
                name = name,
                surname = surname,
                date = date
        )
        db.session.add(student)
        db.session.commit()
        return 'Record was added. {}'.format(student.id)
    except Exception as e:
        return(str(e))


@app.route("/data")
def show_db():
    students = models.Student.query.all()
    print(students)
    return render_template('view.html', students=[st.serialize() for st in students])


# TODO: only accessible for logged in users, otherwise show warning
# Allow enter and submit attendance data if token is correct
@app.route("/qrcode/<token_key>", methods=['GET', 'POST'])
def qr_code_token(token_key):
    token: models.Token = models.token_by_key(token_key)
    form = TokenConfirmForm()
    if not token:
        return render_template("qrcode_token_failed.html",
                               title="Token error",
                               error="This token does not exists")
    if token.expired:
        return render_template("qrcode_token_failed.html",
                               title="Token error",
                               error="this token has expired")
    if form.validate_on_submit():
        models.add_attendance(bs_group=form.group_name.data,
                              name=form.name.data,
                              surname=form.last_name.data)
        return redirect("/index")
    return render_template("qrcode_token.html", token=token, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('data'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('data'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


