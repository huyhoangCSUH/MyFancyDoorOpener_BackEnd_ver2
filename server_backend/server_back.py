#
# This is for server part to handle TCP packets from the RPi
#

import socket
import cv2

from time import sleep
import socket
import os
import time


#HOST = '127.0.0.1'
PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))
sock.listen(10)
print "Start listening on port " + str(PORT)

userhome = os.path.expanduser('~')
path_for_files = userhome + "/MyFancyDoorOpener_BackEnd_ver2/server_backend"

start = time.time()
while 1:
    end = time.time()
    #if end - start > 5:
        # with open(path_for_files + '/person_name.txt', 'w') as f:
        #     name = f.read()
        # with open(path_for_files + '/person_distance.txt', 'w') as f:
        #     distance = f.read()
        # if name_info == 'Huy' and 500 <= distance <= 1500:
        #     with open(path_for_files + '/notification.txt', 'w') as f:
        #         f.write('1')

    #print "listening..."
    try:
        conn, addr = sock.accept()
        pilot_msg = conn.recv(20)
        print("Accepting connection from: " + str(addr))
        print(pilot_msg)

        if pilot_msg == "person_distance":
            conn.close()
            # print "Getting person distance"
            conn2, addr2 = sock.accept()
            distance_msg = conn2.recv(1024)

            conn2.close()

            distance_info = distance_msg.decode('utf-8')
            with open(path_for_files + '/person_distance.txt', 'w') as f:
                f.write(distance_info)

        elif pilot_msg == "person_name":
            conn.close()
            conn2, addr2 = sock.accept()
            name_msg = conn2.recv(1024)
            conn2.close()

            name_info = name_msg.decode('utf-8')
            with open(path_for_files + '/person_name.txt', 'w') as f:
                f.write(name_info)

            if name_info == 'Huy':
                with open(path_for_files + '/notification.txt', 'w') as f:
                    f.write('1')

        elif pilot_msg == "asking_for_auth":
            with open(path_for_files + '/auth_stat.txt') as f:
                auth_code = f.read()
            conn.sendall(auth_code)
            conn.close()

        # elif pilot_msg == "asking_for_framerate":
        #     with open(path_for_files + '/frame_rate.txt') as f:
        #         frame_rate = f.read()
        #     conn.sendall(frame_rate)
        #     conn.close()

    except Exception as msg:
        print str(msg)

print "Done, closing..."
sock.close()

