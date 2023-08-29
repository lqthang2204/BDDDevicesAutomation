import logging
import os
from pathlib import Path


def start_logger_facility():
    Path('output').mkdir(parents=True, exist_ok=True)
    project_folder = os.path.dirname(os.path.dirname(__file__))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(project_folder + '/output/main.log')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    #stream_handler = logging.StreamHandler()
    #stream_handler.setFormatter(formatter)
    #logger.addHandler(stream_handler)

    return logger, project_folder


if __name__ == '__main__':
    logger, project_folder = start_logger_facility()
    logger.info(f'Project Folder: {project_folder}')
    logger.debug('This is a logger Test message')
