from flask import Flask, request as req, jsonify, make_response as res
from api import api

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)