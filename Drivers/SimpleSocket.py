
import string
import socket
import sys
import time


class SimpleSocket:
    def __init__(self, hostname, port=5025, timeout=1):
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.Connect()

    def __del__(self):
        self.sock.close()

    def Connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.hostname, self.port))
            print(self.sock)
        except ValueError:
	        sys.stderr.write("[Socket connection error] Cannot connect to %s, error: %s\n" % (self.hostname, ValueError))
	        sys.exit(2)

    def Close(self):
        self.sock.close()

    def SendCommand(self, cmd):
        self.sock.send((cmd + '\n').encode())

    def Ask(self, cmd):
        self.sock.send((cmd + '\n').encode())
        return self.sock.recv(1024)

    def set_keepalives(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

class DummySocket:
    def __init__(self, hostname, port = 5025):
        print("Initiated")

    def SendCommand(self, cmd):
        pass

    def Ask(self, cmd):
        return ''
