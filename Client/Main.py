from Client import Client
import os

def main():
    user = Client("localhost", 7070)
    user.sendFile("varios.png")

main()


