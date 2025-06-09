import pyotp


class OtpHandler:
    def __init__(self, secret: str, name: str, issuer_name: str = ""):
        self._name = name
        self._issuer_name = issuer_name
        self._totp = pyotp.TOTP(secret)

    def get_uri(self):
        return self._totp.provisioning_uri(
            name=self._name,
            issuer_name=self._issuer_name
        )

    def generate_qr(self):
        try:
            from qrcode.main import QRCode

            qr = QRCode(version=1, box_size=10, border=4)
            qr.add_data(self.get_uri())
            qr.make(fit=True)
            return qr.make_image()
        except ModuleNotFoundError:
            return None

    def verify(self, secret: str) -> bool:
        return self._totp.verify(secret)
