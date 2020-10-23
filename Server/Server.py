import socket, threading, os, json, pickle

class Server:
    
    __HEADER = 128
    __FRAME_SIZE = 1024
    __FORMAT = "utf-8"

    def __init__(self, host, port):
        self.serverAddress = (host, port)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__bind()


    def start(self):
        self.serverSocket.listen()
        while True:
            print(f"[CURRENT ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
            print(f"[LISTENING]...")
            conn, clientAddress = self.serverSocket.accept()
            thread = threading.Thread(target=self.__clientHandler, args=(conn, clientAddress))
            thread.start()

    def __bind(self):
        self.serverSocket.bind(self.serverAddress)

    def __clientHandler(self, conn, address):
        print(f"[NEW CONNECTION] {address} connected.")
        connected = True
        while connected:
            self.__getFile(conn)
            #msg = conn.recv(32).decode(self.__FORMAT)
            #if msg:
            #   print(f"[{address}] : {msg}") """

    def __getFile(self, conn):
        header = self.__getHeader(conn)
        fileName = header["name"]
        frames = header["frames"]
        file = open(fileName, "wb")

        while frames > 0:
            frame = conn.recv(self.__FRAME_SIZE)
            if frame:
                file.write(frame.rstrip())
                frames -= 1
        
        file.close()

    def __getHeader(self, conn):
        stream = conn.recv(self.__HEADER)
        header = pickle.loads(stream)
        return header

