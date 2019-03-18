from flask import render_template, request
from app import app
from app.forms import TokenConfirmForm
from app import db
from app.models import Student


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/qrcode_generate")
def qr_code_generate():
    return render_template("qrcode_generate.html")

@app.route("/add")
def add_student():
    name = request.args.get('name')
    surname = request.args.get('surname')
    date = request.args.get('date')
    try:
        student = Student(
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
    students = Student.query.all()
    return render_template('test.html', string=[st.serialize() for st in students])


@app.route("/qrcode/<token>")
def qr_code_token(token):
    form = TokenConfirmForm()
    return render_template("qrcode_token.html", token=token, form=form)
