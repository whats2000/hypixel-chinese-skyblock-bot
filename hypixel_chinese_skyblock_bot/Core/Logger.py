import logging


class Logger:
    def __init__(self, logger_name: str, log_level: int = logging.INFO):
        console_handle = logging.StreamHandler()
        console_handle.setLevel(log_level)
        console_handle.setFormatter(logging.Formatter('[%(asctime)s / %(name)s / %(levelname)s] %(message)s'))

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handle)

    def log_message(self, log_level: int = logging.DEBUG, message: str = None):
        if log_level == 10:
            self.logger.debug(message)
        elif log_level == 20:
            self.logger.info(message)
        elif log_level == 30:
            self.logger.warning(message)
        elif log_level == 40:
            self.logger.error(message)
        elif log_level == 50:
            self.logger.critical(message)
