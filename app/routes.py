from flask import render_template
from app import app
from app.forms import TokenConfirmForm


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/qrcode_generate")
def qr_code_generate():
    return render_template("qrcode_generate.html")


@app.route("/qrcode/<token>")
def qr_code_token(token):
    form = TokenConfirmForm()
    return render_template("qrcode_token.html", token=token, form=form)
