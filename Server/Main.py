from Server import Server

def main():
    PATH = '/Users/mateosancheztoro/Desktop'
    server = Server("localhost", 8080, PATH)
    server.start()

main()

