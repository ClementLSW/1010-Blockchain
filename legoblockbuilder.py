import socket
import threading

ENCODING = 'utf-8'


class Client(threading.Thread):

    def __init__(self, my_host, my_port):
        threading.Thread.__init__(self, name="message_receiver")
        self.host = my_host
        self.port = my_port

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(10)
        while True:
            connection, client_address = sock.accept()
            try:
                full_message = ""
                while True:
                    data = connection.recv(16)
                    full_message = full_message + data.decode(ENCODING)
                    if not data:
                        print("{}: {}".format(client_address, full_message.strip()))
                        break
            finally:
                connection.shutdown(2)
                connection.close()

    def run(self):
        self.listen()


class Server(threading.Thread):

    def __init__(self, my_friends_host, my_friends_port,my_friends_host1,my_friends_port1):
        threading.Thread.__init__(self, name="message_sender")
        self.host = my_friends_host
        self.port = my_friends_port
        self.host1 = my_friends_host1
        self.port1 = my_friends_port1

    def run(self):
        while True:
            message = input("")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.sendall(message.encode(ENCODING))
            s.shutdown(2)
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host1, self.port1))
            s.sendall(message.encode(ENCODING))
            s.shutdown(2)
            s.close()


def main():
    my_host = input("What is my host(IP address)? ")
    my_port = int(input("What port do I use? "))
    client = Client(my_host, my_port)
    host = input("First host IP address: ")
    port = int(input("First host port: "))
    host1 = input("Second host IP address: ")
    port1 = int(input("Second host port: "))
    server = Server(host, port, host1, port1)
    treads = [client.start(), server.start()]


if __name__ == '__main__':
    main()