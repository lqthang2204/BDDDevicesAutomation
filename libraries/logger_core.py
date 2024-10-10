import logging
import os
from pathlib import Path


def start_logger_facility():
    Path('output').mkdir(parents=True, exist_ok=True)
    project_folder = os.path.dirname(os.path.dirname(__file__))
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    #https://gist.github.com/i0bj/2b3afbe07a44179250474b5f36e7bd9b
    logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.DEBUG, "\033[0;94m%s\033[0m" % logging.getLevelName(logging.DEBUG))
    logging.addLevelName(logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.INFO, "\033[1;32m%s\033[0m" % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.CRITICAL, "\033[4;31m%s\033[0m" % logging.getLevelName(logging.CRITICAL))
    handler = logging.FileHandler(project_folder + '/output/main.log')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, project_folder


if __name__ == '__main__':
    logger, project_folder = start_logger_facility()
    print("test")
    logger.info("test  yhasng")
    logger.info(f'Project Folder: {project_folder}')
    logger.debug('This is a logger Test message')
