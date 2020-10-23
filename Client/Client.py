import socket, os, ast, json, pickle


class Client:

    __FORMAT = "utf-8"
    __FRAME_SIZE = 1024
    __HEADER_SIZE = 128

    def __init__(self, server, port):
        self.serverAddress = (server, port)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect()

    def __connect(self):
        self.clientSocket.connect(self.serverAddress)

    def send(self, message):
        encodedMessage = message.encode(self.__FORMAT)
        self.clientSocket.send(encodedMessage)

    def sendFile(self, filePath):

        file = open(filePath, "rb")
        fileName = file.name
        fileSize = os.path.getsize(filePath)
        frames = int(fileSize/self.__FRAME_SIZE) + 1

        header = {
            "name": fileName,
            "size": fileSize,
            "frames": frames
        }
        self.__sendHeader(pickle.dumps(header))

        for _ in range(frames):
            frame = file.read(self.__FRAME_SIZE)
            self.__sendFrame(frame)

        file.close()

    def __getFile(self, conn):
        header = self.__getHeader(conn)
        fileName = header["name"]
        frames = header["frames"]
        file = open(fileName, "wb")

        while frames > 0:
            frame = self.clientSocket.recv(self.__FRAME_SIZE)
            if frame:
                file.write(frame)
                frames -= 1

        file.close()

    def __getHeader(self, conn):
        stream = self.clientSocket.recv(self.__HEADER_SIZE)
        header = stream.decode(self.__FORMAT)
        return ast.literal_eval(header)

    def __sendHeader(self, header):
        header += b' ' * (self.__HEADER_SIZE - len(header))
        self.clientSocket.send(header)

    def __sendFrame(self, frame):
        frame += b' ' * (self.__FRAME_SIZE - len(frame))
        self.clientSocket.send(frame)
