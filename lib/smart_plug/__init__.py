import importlib
from typing import Type, TypeVar

from lib.smart_plug.abstract_smart_plug import AbstractSmartPlug
from lib.smart_plug.tp_link import HS, KP


__all__ = ["HS", "KP"]
SmartPlug = TypeVar("SmartPlug", HS, KP)
__series_map = {
    "hs": "HS",
    "kp": "KP",
}


def create_smart_plug_instance(
        manufacturer:str,
        series: str,
        *args,
        **kwargs
) -> Type[AbstractSmartPlug]:
    try:
        manufacturer = manufacturer.lower() \
            .replace(" ", "_") \
            .replace("-", "_")
        series = series.lower() \
            .replace(" ", "_") \
            .replace("-", "_")
        module_path = f"lib.smart_plug.{manufacturer}.{series.lower()}"
        module = importlib.import_module(module_path)
        cls = getattr(module, __series_map.get(series))
        return cls(*args, **kwargs)
    except (ImportError, AttributeError) as e:
        raise ImportError(
            f"Could not create instance for manufacturer={manufacturer}, "
            f"series={series}: {e}"
        )
