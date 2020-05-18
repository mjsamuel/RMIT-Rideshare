## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
import cv2, imutils, logging, os

class FaceRecognitionUtil:
    def add_face(self, username, image):
        logging.info("add_face() called")

        # Folder to store user images
        folder = "./socket_server/dataset/{}".format(username)

        # Creating folder for user if it doesn't already exist
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.info("created folder {}".format(folder))

        # Saving
        img_name = "{}/face.jpg".format(folder)
        cv2.imwrite(img_name, image)
        logging.info("created file {}".format(img_name))

    def encode_faces(self):
        pass

    def recognise_face(self):
        pass
