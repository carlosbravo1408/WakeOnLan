import json
import socket
from abc import ABC
from typing import Dict, Any


class AbstractSmartPlug(ABC):
    def __init__(self, host: str, port: int = 9999, timeout=500):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._socket: socket.socket

    def _connect(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        self._socket.settimeout(self._timeout)

    def exec_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        cmd = json.dumps(command)
        try:
            self._connect()
            self._socket.send(self.encrypt(cmd))
            data = self._socket.recv(4096)
        finally:
            if self._socket:
                self._socket.close()
        return self.response(data)

    def encrypt(self, plaintext):
        raise NotImplementedError()

    def decrypt(self, ciphertext):
        raise NotImplementedError()

    def response(self, data):
        _response = self.decrypt(data[4:])
        _response = json.loads(_response)
        _response = _response.get(list(_response)[0])
        _response = _response.get(list(_response)[0])
        return _response

    def turn_on(self):
        raise NotImplementedError()

    def turn_off(self):
        raise NotImplementedError()

    def get_relay_state(self) -> bool:
        raise NotImplementedError()
