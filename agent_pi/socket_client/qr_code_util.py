from pyzbar import pyzbar
import cv2, os, json
import pyqrcode

class QrCodeUtil:
    def decode_qr_code(self, image):
        barcodes = pyzbar.decode(image)
        user_credentials = None
        for barcode in barcodes:
            # the barcode data is a bytes object so we convert it to a string
            barcodeData = barcode.data.decode("utf-8")
            user_credentials = json.loads(barcodeData)

        return user_credentials

    def generate_qr_code(self, username, password):
        data = {
            "username": username,
            "password": password
        }

        encoded_data = pyqrcode.create(json.dumps(data))
        return encoded_data
