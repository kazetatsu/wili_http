#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

import socket
import threading
import time
import struct

req_tr_prob = int.to_bytes(0, 1, 'little', signed=False)

def socket_send_request(request:str, sock_file_path="/tmp/sock.sock", timeout=5.0) -> str | None:
    sock = socket.socket( \
        family=socket.AF_UNIX, \
        type=socket.SOCK_STREAM, \
        proto=0 \
    )
    sock.settimeout(timeout)
    try:
        sock.connect(sock_file_path)
        print("connect")
        time.sleep(0.5)
        sock.send(request.encode())
        print("send")
        responce = sock.recv(1024).decode()
        print("recv")
        sock.shutdown(socket.SHUT_RDWR)
        print("shutdown")
        sock.close()
        return responce
    except Exception as e:
        print(e)
        return None


class SockClient:
    def __init__(self, sock_file_path:str="/tmp/sock.sock"):
        self.sock = socket.socket( \
            family=socket.AF_UNIX, \
            type=socket.SOCK_STREAM, \
            proto=0 \
        )
        self.sock_file_path = sock_file_path
        self.is_conected = self.try_connect(self.sock_file_path)

    def __del__(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except:
            pass

    def try_connect(self, sock_file_path:str) -> bool:
        try:
            self.sock.connect(sock_file_path)
            print('connected socket_bridge !')
            return True
        except ConnectionRefusedError: return False
        except FileNotFoundError: return False

    def send_request(self, req:bytes) -> bytes | None:
        if not self.is_conected:
            self.is_conected = self.try_connect(self.sock_file_path)
        if not self.is_conected: return None

        try:
            self.sock.send(req)
            return self.sock.recv(1024)
        except:
            return None

    def get_tr_prob(self) -> tuple | None:
        res = self.send_request(req_tr_prob)
        if res is None: return None
        # motion num
        n = res[0]
        if n == 0: return (0,)
        fmt = 'f' * (n * n)
        try:
            tr_prob = struct.unpack('<' + fmt, res[1:])
        except ValueError: return None
        else: return (n, list(tr_prob))
