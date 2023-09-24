#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

from flask import Flask, g
from sock_client import SockClient
import numpy as np

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
        return 'res = ' + res.decode()

@app.route("/tr_prob/pretty")
def tr_prob_pretty():
    res = sock_cli.get_tr_prob()
    if res is None:
        return "<p>だめ</p>"
    else:
        return str(np.array(res[1]).reshape((res[0], res[0])))
    

@app.route('/tr_prob')
def tr_prob():
    res = sock_cli.get_tr_prob()
    if res is None:
        return "<p>だめ</p>"
    else:
        n = res[0]
        if n == 0: return '<p>error in wili_bridge</p>'
        tr_prob = res[1]
        ret = []
        for i in range(n):
            ss = [str(a) for a in tr_prob[i * n : (i + 1) * n]]
            ret.append(','.join(ss))
        return '\n'.join(ret)


if __name__ == "__main__":
    sock_cli = SockClient()
    app.run(host="localhost", port=5000)
