import thread
import socket

class gSocketServer:
    def __init__(self,
                addr = '127.0.0.1',
                port = 4000,
                autoChangeAddress = True):
        self.ADDR = addr
        self.PORT = port
        self.autoChangeAddress = autoChangeAddress
        self.ADDRESS = (self.ADDR, self.PORT)
        self.currentUsers = []
        self.listenFlag = False
        self.threads = []

    def _createSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while True:
            try:
                self.sock.bind(self.ADDRESS)
            except socket.error:
                if self.autoChangeAddress:
                    self.PORT += 1
                    self.ADDRESS = (self.ADDR, self.PORT)
                    continue
                else:
                # dont want to increase port automatically
                    raise socket.error
            # bind successfully
            break

        self.sock.listen(5)

    def _closeSocket(self):
        self.sock.close()

    def getCurrentUsers(self):
        return self.currentUsers[:]

    def _connectToAClient(self):
        print 'New connection is waiting'

        conn, addr = self.sock.accept()
        data = None
        self.currentUsers.append(addr)
        self.listenFlag = True

        print str(addr) + " is connected"

        # welcomemessage
        self._handleClientsMessage(conn, addr, str(data))

        while True:
            #get data from client
            data = conn.recv(1024)
            if not data:
                break
            print str(addr) + " " + str(data)

            #send back to the client
            self._handleClientsMessage(conn, addr, str(data) )

        conn.close()
        for tmp in self.currentUsers:
            if tmp == addr:
                self.currentUsers.remove(tmp)
        thread.exit()

    def _handleClientsMessage(self, conn, addre, message):
        welcomeMessage = '''
            Welcome, dear valuable client!
            1 for get current users
            2 for testing
            '''
        if message == '1':
            tmpList =  self.getCurrentUsers()
            tmpString = ""
            for ts in tmpList:
                tmpString += (str(ts) + '\n')
            conn.send(tmpString)
        elif message == '2':
            conn.send('Ok, test')
        else:
            # don't know yet
            conn.send('what is it?')
        #
        conn.send( welcomeMessage )

    def _runCode(self):
        self.listenFlag = False

        self._createSocket()

        t = thread.start_new_thread(self._connectToAClient,())

        while True:

            if self.listenFlag:
                thread.start_new_thread(self._connectToAClient,())
                self.listenFlag = False

        self._closeSocket()
        thread.exit()

    def start(self):
            self._runCode()
