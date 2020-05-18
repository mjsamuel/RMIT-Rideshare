import pytest, mock
from mock import mock_open
from socket_server.face_recognition_util import FaceRecognitionUtil

@pytest.fixture
def fru():
    fru = FaceRecognitionUtil()
    return fru

class TestFaceRecognitionUtil:
    @mock.patch('socket_server.face_recognition_util.cv2.imwrite')
    def test_add_face(self, mock_cv2, fru):
        """Tests to make sure that images are being saved in the correct
        directory
        """
        username = "test"
        save_path = "./socket_server/dataset/" + username + "/face.jpg"
        mock_image = "mock_image"

        fru.add_face(username, mock_image)

        mock_cv2.assert_called_with(save_path, mock_image)
        
    @mock.patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_encode_faces(self, mock_file, fru):
        """Tests to make sure that the encoded faces are being saved to the
        correct directory
        """
        fru.encode_faces()

        mock_file.assert_called_with("./socket_server/encodings.pickle", "wb")
