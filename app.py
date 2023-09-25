#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

from flask import Flask, jsonify
from sock_client import SockClient
from db_client import DBClient
from sqlite3_client import SQLite3Client
import numpy as np
from numpy import ndarray

app = Flask(__name__)
sock_cli:SockClient=None
db_cli:DBClient=None


@app.route("/tr_prob/pretty")
def tr_prob_pretty():
    res = sock_cli.get_tr_prob()
    if not res[0] == 2:
        return res[1], 500
    else:
        return str(res[2]).replace('\n', '<br>')


@app.route('/tr_prob')
def tr_prob():
    result = db_cli.get_tr_prob()
    if result[0] == False:
        return result[1], 500
    else:
        ret = {
            'motion_num': result[1],
            'tr_prob': result[2].tolist(),
        }
        return jsonify(ret)


@app.route('/heatmap')
def heatmap():
    result = db_cli.get_heatmap()
    if result[0] == False:
        return result[1], 500
    else:
        ret = {
            'motion_num': result[1],
            'avr_gaussian': result[2].tolist(),
            'var_gaussian': result[3].tolist(),
        }
        return jsonify(ret)


@app.route('/suggest')
def suggest():
    result = sock_cli.call_suggest()
    if result[0] == False:
        return result[1], 500
    else:
        ret = {
            'motion_num': result[1],
            'weight': result[2].tolist(),
        }
        return jsonify(ret)


if __name__ == "__main__":
    sock_cli = SockClient()
    db_cli = SQLite3Client('/var/lib/wili/test/db.sqlite3')
    app.run(host="localhost", port=5000)
