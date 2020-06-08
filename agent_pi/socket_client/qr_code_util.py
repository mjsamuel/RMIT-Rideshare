from pyzbar import pyzbar
import cv2, os, json
import pyqrcode

class QrCodeUtil:
    def decode_qr_code(self, image):
        """Decodes a supplied QR code as JSON and returns it.

        :param image: The image of qr code
        :type image: numpy.ndarray
        :return: The data encoded in the QR code
        :rtype: dict
        """
        barcodes = pyzbar.decode(image)
        user_credentials = None
        for barcode in barcodes:
            # the barcode data is a bytes object so we convert it to a string
            barcodeData = barcode.data.decode("utf-8")
            user_credentials = json.loads(barcodeData)

        return user_credentials

    def generate_qr_code(self, username, password):
        """Encodes JSON object containg the user's login credentials into a QR
        code.

        :param username: The user's username
        :type username: string
        :param username: The user's password
        :type username: string
        :return: The generated QR code
        :rtype: pyqrcode.QRCode
        """
        data = {
            "username": username,
            "password": password
        }

        encoded_data = pyqrcode.create(json.dumps(data))
        return encoded_data
