from flask import Flask, render_template
from sendMail import mail
from api import api
from os import getenv

app = Flask(__name__)
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=getenv("EMAIL"),
    MAIL_PASSWORD=getenv("EMAIL_PASSWORD")
)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
mail.init_app(app)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)