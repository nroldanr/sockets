import socket, threading

class Server:
    
    def __init__(self, host, port):
        self.serverAddress = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__bind()

    def __bind(self):
        self.socket.bind(self.serverAddress)

    def start(self):
        self.socket.listen()
        while True:
            print(f"[CURRENT ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
            print(f"[LISTENING]...")
            conn, clientAddress = self.socket.accept()
            thread = threading.Thread(target=self.clientHandler, args=(conn, clientAddress))
            thread.start()

    def clientHandler(self, conn, address):
        print(f"[NEW CONNECTION] {address} connected.")
        connected = True
        while connected:
            msg = conn.recv(1024).decode("utf-8")
            if msg:
                print(f"[{address}] : {msg}")