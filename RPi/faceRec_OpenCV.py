import os
import numpy as np
import cv2

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


def predict(frame):
    # Extract the face first
    have_face, face, rect = extract_a_face(frame, 1.2)

    # Then predict it
    label, confidence = face_recognizer.predict(face)

    # get name of respective label returned by face recognizer
    label_text = subjects[label]

    # draw a rectangle around face detected
    #draw_rectangle(frame, rect)
    # draw name of predicted person
    #draw_text(frame, label_text, rect[0], rect[1] - 5)
    return frame, label_text