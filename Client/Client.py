import socket
import pickle
import os
from Commands import Commands


class Client:

    __FORMAT = "utf-8"
    __FILE_FRAME_SIZE = 1024
    __COMMAND_FRAME_SIZE = 32
    __HEADER_SIZE = 128

    def __init__(self, server, port):
        self.serverAddress = (server, port)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect()

    def __connect(self):
        self.clientSocket.connect(self.serverAddress)

        connected = True
        while connected:
            userInput = input('> ').strip()
            self.__action(userInput)
            msg = self.clientSocket.recv(
                self.__COMMAND_FRAME_SIZE).decode(self.__FORMAT)
            if msg:
                print(msg)

    def __sendCommand(self, command, args = ''):
        header = {
            "command": command,
            "args" : args
        }
        self.__sendHeader(pickle.dumps(header))

    def __sendFile(self, filePath):

        file = open(filePath, "rb")
        fileName = file.name
        fileSize = os.path.getsize(filePath)
        frames = int(fileSize/self.__FILE_FRAME_SIZE) + 1

        header = {
            "name": fileName,
            "size": fileSize,
            "frames": frames
        }
        self.__sendHeader(pickle.dumps(header))

        for _ in range(frames):
            frame = file.read(self.__FILE_FRAME_SIZE)
            self.__sendFrame(frame)

        file.close()

    def __getFile(self):
        header = self.__getHeader()
        fileName = header["name"]
        frames = header["frames"]
        file = open(fileName, "wb")

        while frames > 0:
            frame = self.clientSocket.recv(self.__FILE_FRAME_SIZE)
            if frame:
                file.write(frame)
                frames -= 1

        file.close()

    def __getHeader(self):
        stream = self.clientSocket.recv(self.__HEADER_SIZE)
        header = pickle.loads(stream)
        return header

    def __sendHeader(self, header):
        header += b' ' * (self.__HEADER_SIZE - len(header))
        self.clientSocket.send(header)

    def __sendFrame(self, frame):
        frame += b' ' * (self.__FILE_FRAME_SIZE - len(frame))
        self.clientSocket.send(frame)

    def __action(self, msg):
        com = msg.strip().split(" ")
        if com[0] in Commands.__members__:
            command = Commands[com[0]].value

            if command == 1:
                self.__sendCommand(com[0])
            elif command == 2:
                self.__commandVerification(com, 'name')
            elif command == 3:
                self.__commandVerification(com, 'bucket')
            elif command == 4:
                self.__commandVerification(com, 'bucket')
            elif command == 5:
                self.__sendCommand(com[0])
            elif command == 6:
                self.__commandVerification(com, 'file')
            elif command == 7:
                self.__commandVerification(com, 'file')
            elif command == 8:
                self.__commandVerification(com, 'file')
            elif command == 9 or command == 10:
                self.__sendCommand(com[0])
    
    def __commandVerification(self, com, msg):
        if len(com) == 2:
            self.__sendCommand(com[0], com[1])
        else:
            print(f'Unspecified {msg}')
