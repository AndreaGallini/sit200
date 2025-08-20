import logging
from logging.handlers import RotatingFileHandler


# TODO: INSERIRE in ogni modello matematico
def setup_logger():
    # Crea il logger principale
    logger = logging.getLogger('ao1')
    logger.setLevel(logging.WARNING)  # In svilupppo DEBUG, in produzione WARNING

    # Imposta il formato dei messaggi di log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler per la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # File handler con rotazione
    file_handler = RotatingFileHandler('log_ao1.log', maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # Aggiunge gli handler al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
