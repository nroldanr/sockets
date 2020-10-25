import socket
import threading
import os
import json
import pickle
from Commands import Commands


class Server:

    __HEADER = 128
    __FILE_FRAME_SIZE = 1024
    __COMMAND_FRAME_SIZE = 32
    __FORMAT = "utf-8"

    def __init__(self, host, port):
        self.serverAddress = (host, port)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__bind()

    def start(self):
        self.serverSocket.listen()
        while True:
            print(
                f"[CURRENT ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
            print(f"[LISTENING]...")
            conn, clientAddress = self.serverSocket.accept()
            thread = threading.Thread(
                target=self.__clientHandler, args=(conn, clientAddress))
            thread.start()

    def __bind(self):
        self.serverSocket.bind(self.serverAddress)

    def __clientHandler(self, conn, address):
        print(f"[NEW CONNECTION] {address} connected.")
        connected = True
        while connected:
            msg = self.__getHeader(conn)
            if msg:
                self.__action(msg, conn)

    def __sendResponse(self, message, conn):
        encodedMessage = message.encode(self.__FORMAT)
        encodedMessage += b' ' * (self.__COMMAND_FRAME_SIZE - len(encodedMessage))
        conn.send(encodedMessage)

    def __getFile(self, conn):
        header = self.__getHeader(conn)
        fileName = header["name"]
        frames = header["frames"]
        file = open(fileName, "wb")

        while frames > 0:
            frame = conn.recv(self.__FILE_FRAME_SIZE)
            if frame:
                file.write(frame.rstrip())
                frames -= 1

        file.close()

    def __getHeader(self, conn):
        stream = conn.recv(self.__HEADER)
        header = False
        if stream:
            print(stream)
            header = pickle.loads(stream)
        return header

    def __action(self, msg, conn):
        if msg["command"] in Commands.__members__:
            command = Commands[msg["command"]].value

            if command == 1:
                pass
            elif command == 2:
                pass
            elif command == 3:
                pass
            elif command == 4:
                pass
            elif command == 5:
                pass
            elif command == 6:
                self.__getFile(conn)
            elif command == 7:
                pass
            elif command == 8:
                pass
            elif command == 9 or command == 10:
                pass


        self.__sendResponse('respuesta', conn)

