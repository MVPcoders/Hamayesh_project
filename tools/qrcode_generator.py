import qrcode
import os
from hamayeshProject import settings


def qr_code_generator(current_url, cer_id, article_id):
    # Create a QR code
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # size of each box in the QR code
        border=4,  # thickness of the border (minimum is 4)
    )
    qr.add_data(current_url)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Create a directory to save QR codes if it doesn't exist
    qr_code_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    os.makedirs(qr_code_dir, exist_ok=True)

    # Define the file path
    file_name = f"qr_code_{cer_id}_{article_id}.png"
    qr_code_file_path = os.path.join(qr_code_dir, file_name)

    # Save the QR code image
    img.save(qr_code_file_path)

    qr_code_url = os.path.join(settings.MEDIA_URL, 'qr_codes', file_name)

    return qr_code_url
