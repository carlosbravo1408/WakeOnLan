import logging
from typing import Optional


CONSOLE_LOG_HANDLER = logging.StreamHandler()
CONSOLE_LOG_HANDLER.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)


def get_logger(
    name: Optional[str] = None,
    log_level: int = logging.DEBUG,
    propagate: bool = True,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    if not logger.parent.hasHandlers():
        logger.addHandler(CONSOLE_LOG_HANDLER)
    logger.propagate = propagate
    return logger
