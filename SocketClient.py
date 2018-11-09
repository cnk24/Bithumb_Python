import socket

class CSocketClient:
    SERVER_ADDRESS = '127.0.0.1'
    PORT = 24001

    client = None

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client.connect((self.SERVER_ADDRESS, self.PORT))
        except Exception as ex:
            print('Connect Error :', ex)

    def send(self, msg):
        try:
            self.client.send(msg.encode())
        except Exception as ex:
            print('Send Error :', ex)

    def close(self):
        if self.client != None:
            self.client.close()

