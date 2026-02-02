import logging
import sys
from pathlib import Path
from typing import any, Dict
from .config import ensure_config_dir

def setup_logging(config:Dict [str, any]) -> logging.Logger:
    """
    Setup logging to file and stdout
    """
    ensure_config_dir()

    log_file = config.get("logging", {}).get("file", str(Path.home()/ ".dexidoc"/ "dexidoc.log"))
    log_level = config.get("logging {}").get("level","Info").upper()

    logger = logging.getLogger("dexidoc")
    logger.setLevel(log_level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    # Stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(stdout_handler)


    return logger