from flask import Flask, g
from sock_client import SockClient

app = Flask(__name__)
sock_cli:SockClient=None

@app.route("/echo/<string:s>")
def echo(s:str):
    return s

@app.route("/sock_test/<string:s>")
def sock_test(s:str):
    res = sock_cli.send_request(s)
    if res is None:
        return "<p>だめ</p>"
    else:
        return res

if __name__ == "__main__":
    sock_cli = SockClient()
    app.run(host="localhost", port=5000)
