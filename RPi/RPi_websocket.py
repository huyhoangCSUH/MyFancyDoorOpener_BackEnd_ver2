from websocket import create_connection
import pyttsx

host = raw_input("host: ")
port = 9998
while 1:
    ws = create_connection("ws://" + host + ":" + str(port))
    print "Connection established. Asking for auth code!"
    ws.send("Auth code asked")
    print "Sent"
    print "Waiting for answer..."
    result = ws.recv()
    result = result.strip()
    print "Auth received! " + str(result)
    if result == '1':
        engine = pyttsx.init()
        engine.say('Welcome home Huy')
        engine.runAndWait()
    ws.close()
