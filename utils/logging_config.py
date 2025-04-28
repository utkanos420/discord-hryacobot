from loguru import logger
import logging
import sys
import os

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logger.remove()
    logger.add(sys.stdout, level="DEBUG")
    logger.add("logs/logfile.log", level="DEBUG", rotation="10 MB", encoding="utf-8")

    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    setup_library_loggers()

    return logger

def setup_library_loggers():
    libraries = ["uvicorn", "fastapi", "discord"]
    for name in libraries:
        log = logging.getLogger(name)
        log.handlers = [InterceptHandler()]
        log.propagate = False
