from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import time

class SimpleEcho(WebSocket):

    def handleMessage(self):
        while 1:
            time.sleep(1.0)
            with open('input.txt') as f:
                auth_code = f.read().strip()
            if auth_code == '1':
                break
        # echo message back to client
        self.sendMessage(auth_code)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 9998, SimpleEcho)
server.serveforever()
