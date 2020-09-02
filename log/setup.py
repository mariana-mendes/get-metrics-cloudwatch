import logging


def setup_log():
    logger = logging.getLogger("logfile")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('app.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    if(len(logger.handlers) == 0):
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger
