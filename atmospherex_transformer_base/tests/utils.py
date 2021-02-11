import os

from flask import Flask
# https://github.com/SeldonIO/seldon-core/blob/master/python/seldon_core/microservice.py
from seldon_core import wrapper as seldon_microservice
from seldon_core.metrics import SeldonMetrics


def get_test_app(transformer) -> Flask:
    ''' Take a transformer and return a seldon test app '''
    seldon_metrics = SeldonMetrics(worker_id_func=os.getpid)
    transformer.load()
    app = seldon_microservice.get_rest_microservice(transformer, seldon_metrics)
    app.config['TESTING'] = True
    return app
