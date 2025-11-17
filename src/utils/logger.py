"""Configurazione logging per il sistema."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = 'scraper',
    level: str = 'INFO',
    log_file: Optional[str] = None,
    log_to_console: bool = True
) -> logging.Logger:
    """
    Configura e restituisce un logger.

    Args:
        name: Nome del logger
        level: Livello di logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path del file di log (opzionale)
        log_to_console: Se True, logga anche su console

    Returns:
        Logger configurato
    """
    logger = logging.getLogger(name)

    # Converti stringa livello in costante logging
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Rimuovi handlers esistenti per evitare duplicati
    logger.handlers.clear()

    # Formato log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
