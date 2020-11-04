import socket
import pickle
import os
import sys
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

        while not self.clientSocket._closed:
            userInput = input('> ').strip()
            success = self.__action(userInput)
            if (success):
                res = self.__getHeader()
                print(res)

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

        print(frames)

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


    
    def __checkFile(self, filePath):
        if not os.path.exists(filePath):
            print(f'File {filePath} not found')
            return False
        return True


    def __getFile(self):
        header = self.__getHeader()
        fileName = header["name"]
        frames = header["frames"]
        file = open(fileName, "wb")

        print(header)
        while frames > 0:
            frame = self.clientSocket.recv(self.__FILE_FRAME_SIZE)
            if frame:
                file.write(frame)
                frames -= 1

        file.close()

    def __getHeader(self):
        stream = self.clientSocket.recv(self.__HEADER_SIZE)
        header = False
        if stream:
            header = pickle.loads(stream)
        return header

    def __sendHeader(self, header):
        header += b' ' * (self.__HEADER_SIZE - len(header))
        self.clientSocket.send(header)

    def __sendFrame(self, frame):
        frame += b' ' * (self.__FILE_FRAME_SIZE - len(frame))
        self.clientSocket.send(frame)

    def __action(self, msg):
        success = True
        com = msg.strip().split(" ")
        if com[0] in Commands.__members__:
            command = Commands[com[0]].value

            if command == 1:
                self.__sendCommand(com[0])
            elif command == 2:
                goodCom = self.__commandVerification(com, 'name')
                if goodCom:
                    self.__sendCommand(com[0], com[1])
                else:
                    success = False
            elif command == 3:
                goodCom = self.__commandVerification(com, 'bucket')
                if goodCom:
                    self.__sendCommand(com[0], com[1])
                else:
                    success = False
            elif command == 4:
                goodCom = self.__commandVerification(com, 'bucket')
                if goodCom:
                    self.__sendCommand(com[0], com[1])
                else:
                    success = False
            elif command == 5:
                self.__sendCommand(com[0])
            elif command == 6:
                goodCom = self.__commandVerification(com, 'file')
                if goodCom:
                    if self.__checkFile(com[1]):
                        self.__sendCommand(com[0], com[1])
                        self.__sendFile(com[1])
                else:
                    success = False
            elif command == 7:
                goodCom = self.__commandVerification(com, 'file')
                if goodCom:
                    self.__sendCommand(com[0], com[1])

                    confirmation = self.__getHeader()
                    if confirmation == 'file exist':
                        self.__getFile()
                    else:
                        print(confirmation)
                        success = False
                else:
                    success = False

            elif command == 8:
                goodCom = self.__commandVerification(com, 'file')
                if goodCom:
                    self.__sendCommand(com[0], com[1])
                else:
                    success = False
            elif command == 9 or command == 10:
                self.__sendCommand(com[0])
                self.clientSocket.close()
                print('Connection closed')
                sys.exit()

        else:
            print('not a command')
            success = False
        return success
    
    def __commandVerification(self, com, msg):
        if len(com) == 2:
            return True
        else:
            print(f'Unspecified {msg}')
            return False
