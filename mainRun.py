import Ser
import thread

if __name__ == "__main__":
    serverRun = Ser.chatServer()
    thread.start_new_thread( serverRun.start, ())
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

