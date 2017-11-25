import RPi_facerecapi as fr
import cv2
import time
import os
import socket

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

    print "Clean up"
    os.remove("img1.jpg")
    os.remove("img2.jpg")

    print "Now start live recognition, press q anytime to quit"
    start = time.time()
    while 1:
        ret, frame = cam.read()
        if ret:
            frame = cv2.resize(frame, (480, 270))
            cv2.imwrite("img.jpg", frame)

        end = time.time()
        if end - start > 15:
            print "Calling Kairos API"
            person_name = fr.recognize("img.jpg")
            print person_name
            start = time.time()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


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