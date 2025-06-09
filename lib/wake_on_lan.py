import socket
from typing import List, Union

from lib.custom_logger import get_logger


class WakeOnLan:
    logger = get_logger(__name__)

    @classmethod
    def __init__(cls, mac_address: Union[bytes, List[str], str]) -> None:
        cls.wake_on_lan(mac_address)

    @classmethod
    def wake_on_lan(cls, mac_address: Union[bytes, List[str], str]) -> None:
        if isinstance(mac_address, str):
            mac_address = mac_address.replace('-', '') \
                .replace(':', '') \
                .replace('.', '')
            if len(mac_address) != 12:
                raise ValueError(
                    "MAC address string must be 12 hexadecimal characters "
                    "long after removing delimiters."
                )
            try:
                mac_address = bytes.fromhex(mac_address)
            except ValueError:
                raise ValueError(
                    "Invalid hexadecimal characters in MAC address string."
                )
        elif isinstance(mac_address, list):
            if len(mac_address) != 6:
                raise ValueError("MAC address list must contain 6 elements.")
            try:
                mac_address = bytes([int(part, 16) for part in mac_address])
            except ValueError:
                raise ValueError(
                    "Invalid hexadecimal characters in MAC address list."
                )
        elif isinstance(mac_address, bytes):
            if len(mac_address) != 6:
                raise ValueError("MAC address bytes must be 6 bytes long.")
        else:
            raise TypeError(
                "MAC address must be a string, list of strings, or bytes."
            )
        original_mac_str = ":".join(f"{b:02X}" for b in mac_address)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        magic = b"\xff" * 6 + mac_address * 16
        cls.logger.debug(f"Attempting to wake on LAN {original_mac_str}")
        s.sendto(magic, ("<broadcast>", 7))
        s.sendto(magic, ("<broadcast>", 9))
