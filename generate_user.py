from typing import Dict, Any

import pyotp

from lib.db import get_db_session
from models import User, DeviceMac, Device


def add_register(telegram_id: int, name: str, devices: Dict[str, Any]):
    with get_db_session() as session:
        user = session.query(User).get(telegram_id)
        if user is None:
            user = User(
                id_user=telegram_id, name=name, otp_secret=pyotp.random_base32()
            )
            session.add(user)
        for device_name, mac_list in devices.items():
            device = session.query(Device).filter_by(
                name=device_name,
                id_user=telegram_id
            ).first()
            if device is None:
                device = Device(name=device_name, user=user)
                session.add(device)
                session.flush()
            for mac in mac_list:
                existing_mac = session.query(DeviceMac).filter_by(
                    mac_address=mac,
                    id_device=device.id_device
                ).first()
                if existing_mac is None:
                    new_mac = DeviceMac(mac_address=mac, device=device)
                    session.add(new_mac)


if __name__ == "__main__":
    add_register(
        telegram_id=000000,
        name="John",
        devices={
            "Laptop-1": [
                "ac:ac:ac:ac:ac:b8",
                "ac:ac:ac:ac:ac:b9",
            ],
            "Laptop-2": ["84:69:93:6c:b2:22"],
        },
    )

