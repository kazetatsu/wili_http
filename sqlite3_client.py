#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

import sqlite3
import numpy as np

class SQLite3Client:
    def __init__(self, db_path:str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cur = self.conn.cursor()


    def __del__(self):
        self.conn.close()


    def fetch(self, columns:tuple, table:str, order_by:tuple=None) -> list:
        sql = 'SELECT ' + ','.join(columns)
        sql += ' FROM %s' % table
        if not order_by is None:
            sql += ' ORDER BY ' + ','.join(order_by)
        self.cur.execute(sql)
        return self.cur.fetchall()


    def count(self, column:str, table:str) -> int:
        self.cur.execute('SELECT COUNT(%s) FROM %s' % (column, table))
        return self.cur.fetchone()[0]


    def get_tr_prob(self) -> tuple:
        # n := number of motions
        n = self.count('id', 'motion')

        tr_prob = self.fetch(('elem',), 'tr_prob', order_by=('from_motion', 'to_motion'))
        if not len(tr_prob) == n * n:
            return (False, 'too many or few tr_prob records')

        tr_prob = np.array([r[0] for r in tr_prob], dtype='float32')
        tr_prob = tr_prob.reshape((n, n))
        return (True, n, tr_prob)


    def get_heatmap(self) -> tuple:
        n = self.count('id', 'motion')

        gaussian = self.fetch( \
            ('avr_x', 'avr_y', 'var_xx', 'var_xy', 'var_yy'), \
            'gaussian', \
            order_by=('motion',) \
        )
        if not len(gaussian) == n:
            return (False, 'number of gaussian records must be %d. but it is %d.' % (n, len(gaussian)))

        gaussian = np.array(gaussian, dtype='float32')
        return (True, n, gaussian[:, 0:2], gaussian[:, 2:5])
