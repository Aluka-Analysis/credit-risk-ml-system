import logging
import sys
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    Usage: logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # ─── Console Handler ──────────────────────────────
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # ─── Formatter ────────────────────────────────────
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger