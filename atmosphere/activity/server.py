import logging

from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.testclient import TestClient
from pydantic.error_wrappers import ValidationError

from .api.endpoints import Endpoints
from .base_config import Config
from .module_importer import get_module_constructor

logger = logging.getLogger(__name__)
config = Config()
module = get_module_constructor(config)
server = FastAPI()


@server.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)


endpoints = Endpoints(server, module())

if __name__ == "__main__":
    test_client = TestClient(server)
    resp = test_client.get("/versions")
    assert resp.status_code == 200
    logger.info("The server started well")
