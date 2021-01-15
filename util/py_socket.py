from socket import socket, AF_INET, SOCK_STREAM


class SurpacSocketClient:

    def __init__(self, port: object, encode: object):
        self.HOST = 'localhost'
        self.BUFFSIZE = 1024
        self.PORT = port
        self.ENCODE = encode
        self.ADDR = (self.HOST, port)
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
        self.tcpCliSock.connect(self.ADDR)

    def send_message(self, message):
        self.tcpCliSock.sendall(message.encode(self.ENCODE))
        result = self.tcpCliSock.recv(self.BUFFSIZE)
        return result

    def close_socket(self):
        self.tcpCliSock.close()
