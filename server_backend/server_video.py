#
#
# This is for server to handle UDP packets from the RPi (video files)
#
import os
import socket

PORT = 10000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print "Listening for video on port " + str(PORT)
s.bind(('', PORT))

userhome = os.path.expanduser('~')
path_for_files = userhome + "/MyFancyDoorOpener_BackEnd_ver2/server_backend"
buf = 100*1024

while True:

    # Now start receiving the photo
    data, addr = s.recvfrom(buf)
    if data:
        with open(path_for_files + '/video/web_cap.jpg', 'wb') as file_to_write:
            file_to_write.write(data)

