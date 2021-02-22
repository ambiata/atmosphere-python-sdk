import logging
import logging.config
import os
from pathlib import Path

import yaml


class HealthCheckFilter(logging.Filter):
    list_filtered_endpoints = ['GET / ', 'GET /docs/openapi.json ', 'GET /health ', 'GET /status ', 'GET /versions ']

    def filter(self, record):
        if record.name != 'uvicorn.access':
            return True
        for filtered_endpoint in self.list_filtered_endpoints:
            if record.getMessage().find(filtered_endpoint) != -1:
                return False
        return True


class StdErrFilter(logging.Filter):
    """
    Filter for the stderr stream
    Doesn't print records below ERROR to stderr to avoid dupes
    """

    def filter(self, record):
        return record.levelno >= logging.ERROR


class StdOutFilter(logging.Filter):
    """
    Filter for the stdout stream
    Doesn't print records at ERROR or above to stdout to avoid dupes
    """

    def filter(self, record):
        return record.levelno < logging.ERROR


def setup_logging():
    """
    Setup logging configuration
    """
    default_path = 'prod_logging.yaml' if os.getenv('DEBUG', 'False').upper() == 'FALSE' else 'dev_logging.yaml'

    path = Path(__file__).parent / default_path
    with open(path, 'rt') as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)

    logging.info("Loaded logging config from file")
