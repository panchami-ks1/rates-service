import unittest

from flask import Flask

from validator import Validator


class TestValidator(unittest.TestCase):
    def setUp(self):
        # Create an instance of the Flask app and Validator class
        self.app = Flask(__name__)
        self.validator = Validator()

    def test_missing_parameters(self):
        with self.app.app_context():
            # Test case where one or more required parameters are missing
            result, response, status_code = self.validator.validate_input_arguments(
                None, '2023-01-01', 'CNCWN', 'IESNN'
            )
            self.assertFalse(result)
            self.assertEqual(response.json, {"error": "Missing required parameters"})
            self.assertEqual(status_code, 400)

    def test_invalid_date_format(self):
        with self.app.app_context():
            # Test case where the date format is invalid
            result, response, status_code = self.validator.validate_input_arguments(
                'invalid-date', '2023-01-01', 'CNCWN', 'IESNN'
            )
            self.assertFalse(result)
            self.assertEqual(response.json, {"error": "Invalid date format"})
            self.assertEqual(status_code, 400)

    def test_valid_parameters(self):
        with self.app.app_context():
            # Test case where all parameters are valid
            result, response, status_code = self.validator.validate_input_arguments(
                '2023-01-01', '2023-01-31', 'CNCWN', 'IESNN'
            )
            self.assertTrue(result)
            self.assertIsNone(response)
            self.assertIsNone(status_code)


if __name__ == '__main__':
    unittest.main()
