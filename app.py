
from flask import Flask

from service import *


def create_app():
    app = Flask(__name__)
    rate_service = RateService()
    logging.basicConfig(level=logging.DEBUG)

    @app.route('/rates', methods=['GET'])
    def find_rates():
        return rate_service.find_rates()

    # Handle 404 Not Found
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'No data found'}), 404

    # Handle 500 Internal Server Error
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error'}), 500

    return app
