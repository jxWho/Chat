import socket
import thread

ADD = '127.0.0.1'
PORT = 4000
RECEIVE_PORT = 1200
ADDR = (ADD, PORT)
RECEIVE_ADDR = (ADD, RECEIVE_PORT)
class chatClient:
    def __init__(self):
        pass

    def _runCode(self):
        #start a thread to talk to the server
        thread.start_new_thread(_createSocketToTalkToServer,())
        #start a thread to receive message from other clients
        thread.start_new_thread(_createSocketAsServer,())


    def start(self):
        self._runCode()

    #used to talk to the server
    def _createSocketToTalkToServer(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(ADDR)
        while True:
            data = self.s.recv(1024)
            if not data:
                print 'No response from Server'
                break
            elif str(data) == '000':
                #return my socket address
                global RECEIVE_PORT
                self.s.send( RECEIVE_PORT )
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

    # used to be a server and receive message from other clients
    def _createSocketAsServer(self):
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

        while True:
            
