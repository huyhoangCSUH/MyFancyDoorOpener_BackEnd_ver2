from websocket import create_connection
host = raw_input("host: ")
port = 9998
while 1:
    ws = create_connection("ws://" + host + str(port))
    print "Connection established. Asking for auth code!"
    ws.send("Auth code asked")
    print "Sent"
    print "Waiting for answer..."
    result = ws.recv()
    print "Auth received! " + str(result)
    ws.close()
