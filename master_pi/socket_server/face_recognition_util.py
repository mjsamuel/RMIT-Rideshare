## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
import cv2, face_recognition, imutils, pickle, logging, os
from imutils import paths

class FaceRecognitionUtil:
    __DATASET_PATH = "./socket_server/dataset"
    __ENCODINGS_PATH = "./socket_server/encodings.pickle"
    __DETECTION_METHOD = "hog"

    def add_face(self, username, image):
        logging.info("add_face() called")

        # Folder to store user images
        folder = self.__DATASET_PATH + "/{}".format(username)

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
        imagePaths = list(paths.list_images(self.__DATASET_PATH))
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
            boxes = face_recognition.face_locations(rgb, model = self.__DETECTION_METHOD)

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

        with open(self.__ENCODINGS_PATH, "wb") as f:
            f.write(pickle.dumps(data))

    def recognise_face(self, image):
        # load the known faces and embeddings
        logging.info("loading encodings...")
        data = pickle.loads(open(self.__ENCODINGS_PATH, "rb").read())

        # convert the input frame from BGR to RGB then resize it to have
        # a width of 750px (to speedup processing)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(image, width = 240)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input frame, then compute
        # the facial embeddings for each face
        boxes = face_recognition.face_locations(rgb, model = self.__DETECTION_METHOD)
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key = counts.get)

            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for name in names:
            # print to console, identified person
            logging.info("Person found: {}".format(name))
            return name
        logging.info("No match found")
