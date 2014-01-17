import thread
import socket

ADDR = '127.0.0.1'
PORT = 4000
ADDRESS = (ADDR, PORT)

class SocketServer:
    def __init__(self):
        self.currentUsers = []
        self.listenFlag = False
        self.threads = []

    def _createSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(ADDRESS)
        self.sock.listen(5)

    def _closeSocket(self):
        self.sock.close()

    def getCurrentUsers(self):
        return self.currentUsers[:]

    def _connectToAClient(self):
        print 'New connection is waiting'

        conn, addr = self.sock.accept()
        self.currentUsers.append(addr)
        self.listenFlag = True

        print str(addr) + " is connected"

        hint = self._handleClientsMessage(None)
        conn.send(hint)

        while True:
            #get data from client
            data = conn.recv(1024)
            if not data:
                break
            print str(addr) + " " + str(data)

            #send back to the client
            conn.send( self._handleClientsMessage(data) )
            conn.send( self._handleClientsMessage(None))

        conn.close()
        for tmp in self.currentUsers:
            if tmp == addr:
                self.currentUsers.remove(tmp)
        thread.exit()

    def _handleClientsMessage(self, message):
        welcomeMessage = '''
            Welcome, dear valuable client!
            1 for get current users
            2 for testing
            '''
        if message == None:
            return welcomeMessage
        elif message == '1':
            tmpList =  self.getCurrentUsers()
            tmpString = ""
            for ts in tmpList:
                tmpString += (str(ts) + '\n')
            return tmpString
        elif message == '2':
            return 'Ok, test'
        else:
            return welcomeMessage

    def _runCode(self):
        self.listenFlag = False

        self._createSocket()

        t = thread.start_new_thread(self._connectToAClient,())

        while True:

            if self.listenFlag:
                thread.start_new_thread(self._connectToAClient,())
                self.listenFlag = False

        self._closeSocket()

    def start(self):
        thread.start_new_thread(self._runCode,())
