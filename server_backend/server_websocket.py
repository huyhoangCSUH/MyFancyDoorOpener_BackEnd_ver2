from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import time
import os

userhome = os.path.expanduser('~')
path_for_files = userhome + "/MyFancyDoorOpener_BackEnd_ver2/server_backend"

class SimpleEcho(WebSocket):

    def handleMessage(self):
        while 1:
            time.sleep(1.0)
            with open(path_for_files + '/auth_stat.txt') as f:
                auth_code = f.read().strip()
            if auth_code == '1':
                break
        # send authorization to client
        self.sendMessage(auth_code)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 9998, SimpleEcho)
server.serveforever()
