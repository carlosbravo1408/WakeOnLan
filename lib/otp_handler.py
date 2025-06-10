import os

import pyotp


class OtpHandler:
    _issuer_name = os.getenv("ISSUER_HANDLER", "")

    def __init__(self, secret: str, name: str):
        self._name = name
        self._totp = pyotp.TOTP(secret)

    def get_uri(self):
        return self._totp.provisioning_uri(
            name=self._name,
            issuer_name=self._issuer_name
        )

    def verify(self, secret: str) -> bool:
        return self._totp.verify(secret)
