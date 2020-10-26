from Server import Server

def main():
    PATH = '/Users/mateosancheztoro/Desktop/sockets'
    server = Server("localhost", 7070, PATH)
    server.start()

main()
