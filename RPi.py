import os
import numpy as np
from time import sleep
import socket
import sys
import time
import cv2
import VL53L0X


HOST = '45.55.226.236'
PORT = 9999


def send_video_file(file_to_send):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.send("photo")
    print "pilot sent"
    s.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    file_to_send = open(file_to_send, 'rb')
    l = file_to_send.read(1024)
    while l:
        #print 'Sending...'
        s.send(l)
        l = file_to_send.read(1024)
    file_to_send.close()
    s.close()

tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)


def get_distance_from_sensor():
    distance = 0 # in mm
    try:
        distance = tof.get_distance()
        return str(distance)
    except Exception as err:
        print "Error: " + err
        return '0'


    #return str(distance)


def send_distance(distance):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send("person_distance")
    print "person distance sent!"
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(distance)
    s.close()

# cam = Camera()
# time.sleep(1)
#
# while 1:
#     img = cam.getImage()
#     img.save("webcam_cap.jpg")
#     print "Sending a frame"
#     send_video_file("webcam_cap.jpg")
#     time.sleep(1/24)

# Taking distance
# Create a VL53L0X object



# Start streaming webcam
print "Starting camera."
cam = cv2.VideoCapture(0)
time.sleep(1)

print "Start capturing images"
while 1:
    ret, frame = cam.read()
    if ret:
        frame = cv2.resize(frame, (800, 450))
        cv2.imwrite("webcam_cap.jpg", frame)

        print "Sending a frame"

        send_video_file("webcam_cap.jpg")

        # This part will get a person distance from the sensor
        person_distance = get_distance_from_sensor()
        send_distance(person_distance)

        #have_face, face, rect = extract_a_face(frame, 1.2)
        #person_info = ""
        #if have_face:
        #   frame, person = predict(frame)
        #     person_info = "{person: " + person + ", distance: 500mm }"
        # else:
        #     person_info = "{person: none, distance: 0mm}"
        #cv2.imshow("Livestream", frame)

    # Resize before sending

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    time.sleep(2)


cam.release()
cv2.destroyAllWindows()



