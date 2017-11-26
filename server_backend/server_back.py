#
# This is for server part to handle TCP packets from the RPi
#

import socket
import os
import time


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

            users = []
            with open(path_for_files + '/users_list.txt', 'r') as f:
                for line in f:
                    users.append(line.strip())

            if name_info in users:
                with open(path_for_files + '/notification.txt', 'w') as f:
                    f.write('1')

        elif pilot_msg == "asking_for_framerate":
            with open(path_for_files + '/frame_rate.txt') as f:
                frame_rate = f.read()
            conn.sendall(frame_rate)
            conn.close()

        elif pilot_msg == "asking_for_quality":
            with open(path_for_files + '/quality.txt') as f:
                quality = f.read()
            conn.sendall(quality)
            conn.close()

        elif pilot_msg == "add_new_user":
            conn.close()
            conn2, addr2 = sock.accept()
            new_user_name = conn2.recv(1024)
            new_user_name = new_user_name.strip()
            conn2.close()
            with open(path_for_files + '/users_list.txt', 'a+') as f:
                f.write(new_user_name)


    except Exception as msg:
        print str(msg)

print "Done, closing..."
sock.close()

