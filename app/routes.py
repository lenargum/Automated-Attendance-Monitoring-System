from flask import render_template, redirect, url_for, request
from app import app
from app.forms import TokenConfirmForm
from app import db
from app import models


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/qrcode_generate")
def qr_code_generate():
    token = models.get_token()
    if not token:
        return "No good tokens"
    key = token.key
    return render_template("qrcode_generate.html",
                           key=url_for("qr_code_token", token_key=key, _external=app.config["SERVER_URL"]))

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
    return render_template('test.html', string=[st.serialize() for st in students])


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
