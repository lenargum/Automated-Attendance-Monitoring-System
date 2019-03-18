from app import app


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/home")
def home():
    return "Home page test"


@app.route("/qrcode_generate")
def qr_code_generate():
    return "QRCode generation test"


@app.route("/qrcode/<token>")
def qr_code_token(token):
    return "Token test: {}".format(token)
