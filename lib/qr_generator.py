import io
from io import BytesIO
from typing import Optional


def generate_qr(uri: str) -> Optional[BytesIO]:
    try:
        from qrcode.main import QRCode

        qr = QRCode(version=1, box_size=10, border=4)
        qr.add_data(uri)
        qr.make(fit=True)
        qr_img = qr.make_image()
        if qr_img:
            qr_bytes = io.BytesIO()
            qr_img.save(qr_bytes)
            qr_bytes.seek(0)
            return qr_bytes
        return None
    except ModuleNotFoundError:
        return None
