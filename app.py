import logging

from flask import Flask

from service import *


def create_app():
    app = Flask(__name__)
    rate_service = RateService()
    logging.basicConfig(level=logging.DEBUG)

    @app.route('/rates', methods=['GET'])
    def find_rates():
        return rate_service.find_rates()

    return app
