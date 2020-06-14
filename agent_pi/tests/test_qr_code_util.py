import json, pytest, mock, pyqrcode, png, os, cv2
from socket_client.client import Client
from socket_client.qr_code_util import QrCodeUtil


@pytest.fixture
def socket_client():
    socket_client = Client("127.0.0.1", "1")
    return socket_client


class TestQrCodeUtil:


    def test_qr_code_generation(self):
        # Generating QR code
        qr_util = QrCodeUtil()
        qr_code = qr_util.generate_qr_code("engineer", "test")
        qr_code.png("qr_code.png", scale="6")

        # Reading QR code
        image = cv2.imread("qr_code.png")
        data = qr_util.decode_qr_code(image)
        os.remove("qr_code.png")

        # Ensuring data that is read matches the data that has been encoded
        assert(data["username"] == "engineer")
        assert(data["password"] == "test")

