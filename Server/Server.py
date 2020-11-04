import socket
import threading
import os
import json
import pickle
import sys
from Commands import Commands
from Bucket import Bucket


class Server:

    __HEADER = 128
    __FILE_FRAME_SIZE = 1024
    __COMMAND_FRAME_SIZE = 32
    __FORMAT = "utf-8"

    def __init__(self, host, port, bucketsPath):
        self.serverAddress = (host, port)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__bind()
        self.createBucketDir(bucketsPath)
        self.bucketsPath = os.path.join(bucketsPath, 'Buckets')
        self.rootPath = bucketsPath

    def start(self):
        checks = self.__checks()
        if checks:
            self.serverSocket.listen()
            while True:
                print(f"[CURRENT ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
                print(f"[LISTENING]...")
                conn, clientAddress = self.serverSocket.accept()
                buckets = Bucket(self.bucketsPath)
                thread = threading.Thread(
                    target=self.__clientHandler, args=(conn, clientAddress, buckets))
                thread.start()

    def createBucketDir(self, path):
        path = os.path.join(path, 'Buckets')
        self.bucketsCreated = True
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                self.bucketsCreated = False

    def __checks(self):
        if not self.bucketsCreated:
            print(f'Path not found {self.rootPath}')
            print('Please verify your path before trying to start the server')
        if not self.connected:
            print(f'Address {self.serverAddress} already in use')

        return self.bucketsCreated & self.connected

    def __bind(self):
        try:
            self.serverSocket.bind(self.serverAddress)
            self.connected = True
        except:
            self.connected = False

    def __clientHandler(self, conn, address, bucket):
        print(f"[NEW CONNECTION] {address} connected.")
        while not conn._closed:
            msg = self.__getHeader(conn)
            if msg:
                self.__action(msg, conn, bucket)
        print(f'Client {address} disconnected')
        print(f"[CURRENT ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
        sys.exit()

    def __sendResponse(self, message, conn):
        encodedMessage = message.encode(self.__FORMAT)
        encodedMessage += b' ' * \
            (self.__COMMAND_FRAME_SIZE - len(encodedMessage))
        conn.send(encodedMessage)

    def __getFile(self, conn, file):
        header = self.__getHeader(conn)
        frames = header["frames"]

        print(header)

        while frames > 0:
            frame = conn.recv(self.__FILE_FRAME_SIZE)
            if frame:
                file.write(frame.rstrip())
                frames -= 1

        file.close()

    def __sendFile(self, file, conn):

        fileName = os.path.basename(file.name)
        print(fileName)
        fileSize = os.path.getsize(os.path.realpath(file.name))
        frames = int(fileSize/self.__FILE_FRAME_SIZE) + 1

        header = {
            "name": fileName,
            "size": fileSize,
            "frames": frames
        }
        self.__sendHeader(pickle.dumps(header), conn)

        for _ in range(frames):
            frame = file.read(self.__FILE_FRAME_SIZE)
            self.__sendFrame(frame, conn)

        file.close()

    def __sendHeader(self, header, conn):
        header += b' ' * (self.__HEADER - len(header))
        conn.send(header)

    def __sendFrame(self, frame, conn):
        frame += b' ' * (self.__FILE_FRAME_SIZE - len(frame))
        conn.send(frame)

    def __getHeader(self, conn):
        stream = conn.recv(self.__HEADER)
        header = False
        if stream:
            header = pickle.loads(stream)
        return header

    def __action(self, msg, conn, bucket):
        if msg["command"] in Commands.__members__:
            command = Commands[msg["command"]].value

            if command == 1:
                message = pickle.dumps(bucket.bList())
                self.__sendHeader(message, conn)
            elif command == 2:
                args = msg['args']
                bucket.bNew(args)
                message = pickle.dumps(f'Bucket {args} created')
                self.__sendHeader(message, conn)
            elif command == 3:
                args = msg['args']
                bucket.bSelect(args)
                message = pickle.dumps(f'Switched to bucket {args}')
                self.__sendHeader(message, conn)
            elif command == 4:
                args = msg['args']
                bucket.bDelete(args)
                message = pickle.dumps(f'Bucket {args} deleted')
                self.__sendHeader(message, conn)
            elif command == 5:
                message = pickle.dumps(bucket.fList())
                self.__sendHeader(message, conn)
            elif command == 6:
                args = msg['args']
                file = bucket.fUpload(args)
                self.__getFile(conn, file)
                message = pickle.dumps(f'File uploaded')
                self.__sendHeader(message, conn)

            elif command == 7:
                args = msg['args']
                if bucket.checkFile(msg['args']):   
                    message = pickle.dumps(f'file exist')
                    self.__sendHeader(message, conn)
                    file = bucket.fDownload(args)
                    self.__sendFile(file, conn)
                    message = pickle.dumps(f'file downloaded')
                    self.__sendHeader(message, conn)
                else:
                    message = pickle.dumps(f'file does not exist')
                    self.__sendHeader(message, conn)

            elif command == 8:
                args = msg['args']
                bucket.fDelete(args)
                message = pickle.dumps(f'File {args} deleted')
                self.__sendHeader(message, conn)

            elif command == 9 or command == 10:
                conn.close()
            else:
                message = pickle.dumps(f'Bad command')
                self.__sendHeader(message, conn)
