from flask import Flask

app = Flask(__name__)

@app.route("/echo/<string:s>")
def echo(s:str):
    return s

