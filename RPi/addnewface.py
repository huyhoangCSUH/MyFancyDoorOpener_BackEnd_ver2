import RPi_facerecapi as fr
import cv2
import time
import os
import socket
import json

HOST = raw_input("Server address: ")
PORT = 9999

def main():
    print "The camera will take two photos. Keep your head still."
    cam = cv2.VideoCapture(0)
    time.sleep(2)

    ret, frame = cam.read()
    cv2.imwrite("img1.jpg", frame)

    time.sleep(2)

    ret, frame = cam.read()
    cv2.imwrite("img2.jpg", frame)

    print "Done."
    new_name = raw_input("New user's name: ")

    response = fr.enroll("img1.jpg", new_name)
    if 'Errors' in response:
        print response["Errors"][0]["message"]
    else:
        print "Successfully enrolled to Kairos API, now verifying"

    response = fr.verify("img2.jpg", new_name)
    if 'Errors' in response:
        print response["Errors"][0]["message"]
    else:
        print "Verification complete."

    add_new_user(new_name)
    print "new user added"


def add_new_user(person_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send("add_new_user")
    s.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(person_name)
    s.close()


main()