from socket import socket, AF_INET, SOCK_STREAM


class SurpacSocketClient:

    def __init__(self, port: object, encode: object):
        self.HOST = 'localhost'
        self.BUFSIZ = 1024
        self.PORT = port
        self.ENCODE = encode
        self.ADDR = (self.HOST, port)
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
        self.tcpCliSock.connect(self.ADDR)

    def sendMsg(self, msg):
        self.tcpCliSock.sendall(msg.encode(self.ENCODE))
        result = self.tcpCliSock.recv(self.BUFSIZ)
        return result

    def closeSocket(self):
        self.tcpCliSock.close()

