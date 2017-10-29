import socket
import cv2
import os
import numpy as np
from time import sleep
import socket
import sys
import time

subjects = ["Huy Hoang", "Tahsin", "Yong Li"]

face_recognizer = cv2.face.createLBPHFaceRecognizer()


def extract_a_face(img, scalefact):
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        '/home/huy/opencv/data/lbpcascades/lbpcascade_frontalface.xml')

    faces = face_cascade.detectMultiScale(gray, scaleFactor=scalefact, minNeighbors=5, minSize=(100, 100));

    # if no faces are detected then return original img
    if len(faces) == 0:
        return 0, None, None

    (x, y, w, h) = faces[0]

    # return only the face part of the image
    return 1, gray[y:y + w, x:x + h], faces[0]


if not os.path.exists("trained_faces/trained_faces.yml"):
    print "No trained faces detected!"

    def prepare_training_data(data_folder_path):

        dirs = os.listdir(data_folder_path)
        faces = []
        labels = []

        for dir_name in dirs:
            if not dir_name.startswith("person"):
                continue
            label = int(dir_name.replace("person", ""))
            subject_dir_path = data_folder_path + "/" + dir_name

            # get the images names that are inside the given subject directory
            subject_images_names = os.listdir(subject_dir_path)

            for image_name in subject_images_names:

                # ignore system files like .DS_Store
                if image_name.startswith("."):
                    continue

                # build image path
                # sample image path = training-data/s1/1.pgm
                image_path = subject_dir_path + "/" + image_name

                # read image
                image = cv2.imread(image_path)

                # detect face
                have_face, face, rect = extract_a_face(image, 1.05)

                if have_face:
                    faces.append(face)
                    labels.append(label)

        return faces, labels

    print("Feeding training data...")
    faces, labels = prepare_training_data("training-data")

    face_recognizer.train(faces, np.array(labels))
    print "Finished training, saving the recognizer..."
    face_recognizer.save("trained_faces/trained_faces.yml")


face_recognizer.load("trained_faces/trained_faces.yml")
print "Trained data loaded!"


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


def predict(img):
    # predict the image using our face recognizer
    label, confidence = face_recognizer.predict(face)
    # get name of respective label returned by face recognizer
    label_text = subjects[label]

    # draw a rectangle around face detected
    draw_rectangle(img, rect)
    # draw name of predicted person
    draw_text(img, label_text, rect[0], rect[1] - 5)
    return img, label_text

#HOST = '127.0.0.1'
PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))
sock.listen(10)
print "Start listening on port " + str(PORT)

path_for_files = "/home/huy/MyFancyDoorOpener_BackEnd_ver2/server_backend"

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

        elif pilot_msg == "photo":
            conn.close()
            conn2, addr2 = sock.accept()
            # print "Getting person photo"

            with open(path_for_files + '/video/web_cap.jpg', 'wb') as file_to_write:
                while True:
                    data = conn2.recv(1024)
                        #print data
                    if not data:
                        break
                    file_to_write.write(data)

            # print "File received!"
            conn2.close()

            # Start detecting the person
            frame = cv2.imread(path_for_files + '/video/web_cap.jpg')
            have_face, face, rect = extract_a_face(frame, 1.2)
            person = 'Undetected'
            if have_face:
                frame, person = predict(frame)
            print person
            with open(path_for_files + '/person_name.txt', 'w') as f:
                f.write(person)

            cv2.imwrite(path_for_files + '/video/web_cap.jpg', frame)

        elif pilot_msg == "asking_for_auth":
            with open(path_for_files + '/auth_stat.txt') as f:
                auth_code = f.read()
            conn.sendall(auth_code)
            conn.close()


    except Exception as msg:
        print str(msg)

print "Done, closing..."
sock.close()

