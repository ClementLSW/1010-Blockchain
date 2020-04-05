import datetime
import hashlib
import socket
import threading
from time import time
from hashlib import sha256
import json

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
                    data = connection.recv(9000)
                    #full_message = full_message + data.decode(ENCODING)
                    jsonfile = data.decode()
                    data = json.loads(jsonfile)
                    blockchain = data.get("chain")
                    if not data:
                        print(blockchain)
                        #print("{}: {}".format(client_address, full_message.strip()))
                        break
            finally:
                connection.shutdown(2)
                connection.close()

    def run(self):
        self.listen()


class Server(threading.Thread):

    def __init__(self, my_friends_host, my_friends_port, my_friends_host1, my_friends_port1):
        threading.Thread.__init__(self, name="message_sender")
        self.host = my_friends_host
        self.port = my_friends_port
        self.host1 = my_friends_host1
        self.port1 = my_friends_port1

    def run(self):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            blockchain = Blockchain()
            name = input("What is your name? ")
            t1 = blockchain.new_transaction(name)
            blockchain.new_block(12345)
            data = json.dumps({"chain": blockchain.chain})
            s.sendall(data.encode())
            #s.sendall(message.encode(ENCODING))
            s.shutdown(2)
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host1, self.port1))
            blockchain = Blockchain()
            name = input("What is your name? ")
            t1 = blockchain.new_transaction(name)
            blockchain.new_block(12345)
            data = json.dumps({"chain": blockchain.chain})
            s.sendall(data.encode())
            #s.sendall(message.encode(ENCODING))
            s.shutdown(2)
            s.close()


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(data ="Genesis", previous_hash="asda")

    # Create a new block listing key/value pairs of block information in a JSON object. Reset the list of pending transactions & append the newest block to the chain.

    def new_block(self, data, previous_hash=None):
        unhashedblock = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': data,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': data,
            'hash value': hash(json.dumps(unhashedblock, sort_keys=True)),
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)

        print(block)

        return block

    # Search the blockchain for the most recent block.

    @property
    def last_block(self):
        return self.chain[-1]

    # Add a transaction with relevant info to the 'blockpool' - list of pending tx's.

    def new_transaction(self, my_name):
        transaction = {
            'name': my_name
            #'joke': recipient,
            #'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    # receive one block. Turn it into a string, turn that into Unicode (for hashing). Hash with SHA256 encryption, then translate the Unicode into a hexidecimal string.

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash


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

    exit = False

    while exit == False:
        blockchain = Blockchain()
        command = input("What would you like to do?\nEnter the corresponding number\n\n1. Add new block\n2. Sync all blocks\n3. Query latest block\n4. Query timestamp of block\n5. Exit\n\n")
        if command == "1":
            inData = input("What data would you like to store? ")
            blockchain.new_block(data=inData)
            # Code to sync blockchain amongst nodes
        elif command == "2":
            blockchain.new_block()
        elif command == "3":
            blockchain.last_block()
        elif command == "4":
             # Code to retrieve timestamp by index
            blockchain.new_block(data=time())

        elif command == 5:
            exit = True


if __name__ == '__main__':
    main()
