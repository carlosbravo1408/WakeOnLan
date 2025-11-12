"""
This class only works with the Tp-Link Kasa SmartPlugs HS10x series.
Command list:
https://github.com/softScheck/tplink-smartplug/blob/master/tplink-smarthome-commands.txt
Taken from:
https://www.softscheck.com/en/blog/tp-link-reverse-engineering/
"""

import struct

from lib.smart_plug.abstract_smart_plug import AbstractSmartPlug


class HS(AbstractSmartPlug):

    def encrypt(self, plaintext):
        key = 171
        plainbytes = plaintext.encode()
        buffer = bytearray(struct.pack('>I', len(plainbytes)))
        for plainbyte in plainbytes:
            cipherbyte = key ^ plainbyte
            key = cipherbyte
            buffer.append(cipherbyte)
        return bytes(buffer)

    def decrypt(self, ciphertext):
        key = 171
        buffer = []
        for cipherbyte in ciphertext:
            plainbyte = key ^ cipherbyte
            key = cipherbyte
            buffer.append(plainbyte)
        plaintext = bytes(buffer)
        return plaintext.decode()


    def turn_on(self):
        _command = {"system": {"set_relay_state": {"state": 1}}}
        return self.exec_command(_command)

    def turn_off(self):
        _command = {"system": {"set_relay_state": {"state": 0}}}
        return self.exec_command(_command)

    def get_relay_state(self) -> bool:
        _command = {"system":{"get_sysinfo":None}}
        _data = self.exec_command(_command)
        return bool(_data.get("relay_state", 0))
