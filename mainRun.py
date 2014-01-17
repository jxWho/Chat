import Ser

if __name__ == "__main__":
    serverRun = Ser.SocketServer()
    serverRun.start()
    hint = '''
    0 to 'exit'
    1 to see current clients
    '''
    while True:
        data = raw_input(hint)
        if data == '0':
            break
        elif data == '1':
            Cclients = serverRun.getCurrentUsers()

