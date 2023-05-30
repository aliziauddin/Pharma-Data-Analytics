import sys
from loguru import logger
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def myLogger():
    logger.remove(0)
    logger.add(
        sys.stderr, format="{time} - <red>[{level}]</red> Message : <green>{message}</green>", colorize=True)

    logger.add(f'{THIS_FOLDER}/out.log', rotation="100 MB")
    return logger
