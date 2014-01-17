import socket

ADD = '127.0.0.1'
PORT = 4000
RECEIVE_PORT = 1200
ADDR = (ADD, PORT)
RECEIVE_ADDR = (ADD, RECEIVE_PORT)
class chatClient:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _runCode(self):
        self.s.connect(ADDR)
        while True:
            data = self.s.recv(1024)
            if not data:
                print 'No response from Server'
                break
            else:
                print str(data)

            msg = raw_input('Please input your message(empty message to end):')
            if not msg:
                break
            self.s.send(msg)
            data = self.s.recv(1024)
            if not data:
                break
            print str(data)
        self.s.close()

    def start(self):
        self._runCode()

    def _createSocket(self):
        self.receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiveSocket.setsockopt(socket.SOL_SOCKET,
                                    socket.SO_REUSEADDR,1)
        while True:
            try:
                global RECEIVE_ADDR
                global RECEIVE_PORT
                self.receiveSocket.bind(RECEIVE_ADDR)
            except socket.error:
                RECEIVE_PORT+=1
                RECEIVE_ADDR = (ADD, RECEIVE_PORT)
                continue
            #when bind succeed
            break

        self.receiveSocket.listen(5)

