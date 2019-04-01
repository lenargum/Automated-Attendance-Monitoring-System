from flask import render_template, redirect, url_for, request, jsonify
from app import app
from app.forms import TokenConfirmForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app import qrcode
from app import models


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/qrcode_generate")
def qr_code_generate():
    return render_template("qrcode_generate.html")


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


@app.route("/qrcode_regen")
def regen():
    models.reset_token()
    return "ok"


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
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile/<email>')
@login_required
def profile(email):
    user = models.User.query.filter_by(email=email).first_or_404()
    print(user.id)
    return render_template('profile.html', user=user)


