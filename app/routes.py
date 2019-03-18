from flask import render_template
from app import app
from app.forms import TokenConfirmForm
from app import models


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/qrcode_generate")
def qr_code_generate():
    return render_template("qrcode_generate.html")


@app.route("/qrcode/<token_key>")
def qr_code_token(token_key):
    token: models.Token = models.token_by_key(token_key)
    if not token:
        return render_template("qrcode_token_failed.html",
                               title="Token error",
                               error="This token does not exists")
    if token.expired:
        return render_template("qrcode_token_failed.html",
                               title="Token error",
                               error="this token has expired")
    form = TokenConfirmForm()
    return render_template("qrcode_token.html", token=token, form=form)
