import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from flask import Flask

from src.services.service import RateService


class TestRateService(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()
        self.rate_service = RateService()

    @patch('src.services.service.psycopg2.connect')
    @patch('src.services.service.get_ports')
    @patch('src.services.service.get_average_price')
    def test_find_rates_successful(self, mock_get_average_price, mock_get_ports, mock_connect):
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock get_ports to return a list of ports
        mock_get_ports.side_effect = [
            ['CNSGH'],
            ['USNYC']
        ]

        # Mock get_average_price to return a list of prices
        mock_get_average_price.return_value = [
            (datetime(2023, 8, 1), 1000),
            (datetime(2023, 8, 2), 1200),
            (datetime(2023, 8, 3), 1100),
            (datetime(2023, 8, 4), 1150),
            (datetime(2023, 8, 5), 1080)
        ]

        with self.app.test_request_context('/rates?date_from=2023-08-01&date_to=2023-08-05&origin=CNSGH&destination=USNYC'):
            response = self.rate_service.find_rates()

        expected_response = [
            {"day": "2023-08-01", "average_price": 1000},
            {"day": "2023-08-02", "average_price": 1200},
            {"day": "2023-08-03", "average_price": 1100},
            {"day": "2023-08-04", "average_price": 1150},
            {"day": "2023-08-05", "average_price": 1080},
        ]
        self.assertEqual(response.json, expected_response)

    @patch('src.services.service.psycopg2.connect')
    @patch('src.services.service.get_ports')
    @patch('src.services.service.get_average_price')
    def test_find_rates_no_data(self, mock_get_average_price, mock_get_ports, mock_connect):
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock get_ports to return a list of ports
        mock_get_ports.side_effect = [
            ['CNSGH'],
            ['USNYC']
        ]

        # Mock get_average_price to return an empty list (no data)
        mock_get_average_price.return_value = []

        with self.app.test_request_context('/rates?date_from=2023-08-01&date_to=2023-08-05&origin=CNSGH&destination=USNYC'):
            response = self.rate_service.find_rates()

        expected_response = [
            {"day": "2023-08-01", "average_price": None},
            {"day": "2023-08-02", "average_price": None},
            {"day": "2023-08-03", "average_price": None},
            {"day": "2023-08-04", "average_price": None},
            {"day": "2023-08-05", "average_price": None},
        ]
        self.assertEqual(response.json, expected_response)

    @patch('src.services.service.psycopg2.connect')
    @patch('src.services.service.get_ports')
    @patch('src.services.service.Validator.validate_input_arguments')
    def test_find_rates_validation_failure(self, mock_validate_input, mock_get_ports, mock_connect):
        # Mock the validation to fail
        mock_validate_input.return_value = (False, 'Validation failed', 400)

        with self.app.test_request_context('/rates?date_from=2023-08-01&date_to=2023-08-05&origin=CNSGH&destination=USNYC'):
            message, code = self.rate_service.find_rates()

        self.assertEqual(message, 'Validation failed')
        self.assertEqual(code, 400)

if __name__ == '__main__':
    unittest.main()
