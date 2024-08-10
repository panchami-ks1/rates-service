import logging
from datetime import datetime

from flask import jsonify


class Validator:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_input_arguments(self, date_from, date_to, origin, destination):
        if not all([date_from, date_to, origin, destination]):
            self.logger.info("Missing one or more parameters.")
            return False, jsonify({"error": "Missing required parameters"}), 400

        try:
            datetime.strptime(date_from, '%Y-%m-%d').date()
            datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            self.logger.info("Invalid date format.")
            return False, jsonify({"error": "Invalid date format"}), 400

        return True, None, None
