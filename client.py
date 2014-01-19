# A class which is designed to talk to the server
import socket
import thread

class chatClient:
    def __init__(self, add = '127.0.0.1', port = 4000):
        self.ADD = add
        self.PORT = port
        self.ADDR = (self.ADD, self.PORT)

    def _runCode(self):
        #start a thread to talk to the server
        self._createSocketToTalkToServer()


    def start(self):
        self._runCode()

    def stop(self):
        self.s.close()
        self.s = None

    def _receiveMessage(self):
        while True:
            if not self.s:
                break
            data = self.s.recv(1024)
            if not data:
                continue
            else:
                print str(data)
        thread.exit()

    def _sendMessage(self):
        while True:
            if not self.s:
                break
            msg = raw_input('anything to talk to the server?:')
            if not msg:
                continue
            self.s.send(msg)

        thread.exit()

    #used to talk to the server
    def _createSocketToTalkToServer(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'sdfdf'
        try:
            self.s.connect(self.ADDR)
        except socket.error:
            print 'cannot connect to the server'
            return

        thread.start_new_thread(self._sendMessage,() )
        self._receiveMessage()


    def _handleMessage(self):
        while True:
            data = self.s.recv(1024)
            if not data:
                print 'No response from Server'
                break
            elif str(data) == '000':
                #return my socket address
                pass
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

