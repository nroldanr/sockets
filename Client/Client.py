import socket

class Client:

    def __init__(self, server, port):
        self.serverAddress = (server, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect()

    def __connect(self):
        self.socket.connect(self.serverAddress)

    def send(self, message):
        encodedMessage = message.encode("utf-8")
        self.socket.send(encodedMessage)

user = Client("localhost", 7070)
user.send("Hello")

