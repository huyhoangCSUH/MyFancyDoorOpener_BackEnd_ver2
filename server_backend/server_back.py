#
# This is for server part to handle TCP packets from the RPi
#

import socket
import cv2

from time import sleep
import socket
import os
import time
import faceRec_API as fr


#HOST = '127.0.0.1'
PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))
sock.listen(10)
print "Start listening on port " + str(PORT)

userhome = os.path.expanduser('~')
path_for_files = userhome + "/MyFancyDoorOpener_BackEnd_ver2/server_backend"


while 1:
    #rint "listening..."
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
            #print(auth_msg)
            conn2.close()

            distance_info = distance_msg.decode('utf-8')
            with open(path_for_files + '/person_distance.txt', 'w') as f:
                f.write(distance_info)

        # elif pilot_msg == "photo":
        #     conn.close()
        #     conn2, addr2 = sock.accept()
        #     # print "Getting person photo"
        #
        #     with open(path_for_files + '/video/web_cap.jpg', 'wb') as file_to_write:
        #         while True:
        #             data = conn2.recv(5*1024)
        #                 #print data
        #             if not data:
        #                 break
        #             file_to_write.write(data)
        #
        #     # print "File received!"
        #     conn2.close()

            # Start detecting the person
            #frame = cv2.imread(path_for_files + '/video/web_cap.jpg')
            #have_face, face, rect = fr.extract_a_face(frame, 1.2)
            #person = 'Undetected'
            #if have_face:
            #    frame, person = fr.predict(frame)
            #print person
            #with open(path_for_files + '/person_name.txt', 'w') as f:
            #    f.write(person)

            #cv2.imwrite(path_for_files + '/video/web_cap.jpg', frame)

        elif pilot_msg == "asking_for_auth":
            with open(path_for_files + '/auth_stat.txt') as f:
                auth_code = f.read()
            conn.sendall(auth_code)
            conn.close()

        elif pilot_msg == "asking_for_framerate":
            with open(path_for_files + '/frame_rate.txt') as f:
                frame_rate = f.read()
            conn.sendall(frame_rate)
            conn.close()


    except Exception as msg:
        print str(msg)

print "Done, closing..."
sock.close()

