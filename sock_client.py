import socket
import threading
import time

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
            return True
        except ConnectionRefusedError: return False
        except FileNotFoundError: return False

    def send_request(self, req:str) -> str | None:
        if not self.is_conected:
            self.is_conected = self.try_connect(self.sock_file_path)
        if not self.is_conected: return None

        try:
            self.sock.send(req.encode())
            return self.sock.recv(1024).decode()
        except:
            return None
