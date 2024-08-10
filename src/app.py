from flask import Flask

from src.services.service import *
from flask_caching import Cache
from src.config.config import config

app = Flask(__name__)
app.config['CACHE_TYPE'] = config.CACHE_TYPE
app.config['CACHE_REDIS_HOST'] = config.CACHE_REDIS_HOST
app.config['CACHE_REDIS_PORT'] = config.CACHE_REDIS_PORT
app.config['CACHE_DEFAULT_TIMEOUT'] = config.CACHE_DEFAULT_TIMEOUT  # Cache timeout in seconds (e.g., 5 minutes)

cache = Cache(app)

rate_service = RateService()
logging.basicConfig(level=logging.DEBUG)


@app.route('/rates', methods=['GET'])
@cache.cached(timeout=config.CACHE_DEFAULT_TIMEOUT, query_string=True)  # Cache with a timeout of 300 seconds
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


if __name__ == '__main__':
    app.run(debug=True)
