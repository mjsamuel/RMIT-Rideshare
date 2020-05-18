## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
import cv2, face_recognition, pickle, logging, os
from imutils import paths

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
        logging.info("encode_faces() called")

        # grab the paths to the input images in our dataset
        imagePaths = list(paths.list_images("./socket_server/dataset"))
        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            logging.info("processing image {}/{}".format(i + 1, len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model = "hog")

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and encodings
                knownEncodings.append(encoding)
                knownNames.append(name)

        # dump the facial encodings + names to disk
        logging.info("serializing encodings...")
        data = { "encodings": knownEncodings, "names": knownNames }

        with open("./socket_server/encodings.pickle", "wb") as f:
            f.write(pickle.dumps(data))

    def recognise_face(self):
        pass
