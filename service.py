import os
from datetime import timedelta

import psycopg2
from flask import request

from validator import *

PG_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:ratestask@localhost:5432/postgres')


class RateService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.validator = Validator()

    def find_rates(self):
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        self.logger.info(
            f"requests received to find rates, origin={origin}, destination={destination}, from={date_from} and to={date_to}")
        success, message, code = self.validator.validate_input_arguments(date_from, date_to, origin, destination)
        if not success:
            # Validation failed, returning back the error message.
            return message, code
        # Establish database connectivity.
        db = psycopg2.connect(PG_DATABASE_URI)
        cursor = db.cursor()

        origin_ports = get_ports(cursor, origin)
        destination_ports = get_ports(cursor, destination)
        self.logger.info(
            f"fetched port data from DB, origin_ports={origin_ports} and destination_ports={destination_ports}")
        if not origin_ports or not destination_ports:
            self.logger.info("Origin port or Destination port does not exist ")
            return jsonify({"error": "Origin port or Destination port does not exist."})
        price_list = get_average_price(cursor, origin_ports, destination_ports, date_from, date_to)
        self.logger.info(f"fetched price data from DB, size={len(price_list)}")
        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        # Get all dates between date_from and date_to
        date_list = [(date_from + timedelta(days=x)).strftime('%Y-%m-%d') for x in
                     range((date_to - date_from).days + 1)]
        # Create a dictionary from the query result with date as the key
        result_dict = {row[0].strftime('%Y-%m-%d'): row[1] for row in price_list}
        # Prepare the response list by iterating over all dates
        response = []
        for day in date_list:
            if day in result_dict:
                response.append({
                    "day": day,
                    "average_price": result_dict[day]
                })
            else:
                response.append({
                    "day": day,
                    "average_price": None  # No data for this day
                })

        return jsonify(response)


def get_ports(cursor, identifier):
    if len(identifier) == 5:
        # It's a port code
        return [identifier]
    else:
        # It's a region slug, find all ports in the region recursively
        query = """
        WITH RECURSIVE region_tree AS (
            SELECT slug
            FROM regions
            WHERE slug = %s
            UNION ALL
            SELECT r.slug
            FROM regions r
            JOIN region_tree rt ON r.parent_slug = rt.slug
        )
        SELECT code FROM ports WHERE parent_slug IN (SELECT slug FROM region_tree)
        """
        cursor.execute(query, (identifier,))
        ports = cursor.fetchall()
        return [port[0] for port in ports]


def get_average_price(cursor, origin_ports, destination_ports, date_from, date_to):
    query = """
        SELECT day, ROUND(AVG(price)) as avg_price
        FROM prices
        WHERE day BETWEEN %s AND %s
        AND orig_code IN ({})
        AND dest_code IN ({})
        GROUP BY day
        HAVING COUNT(price) >= 3
        ORDER BY day
        """.format(
        ','.join('%s' for _ in origin_ports),
        ','.join('%s' for _ in destination_ports)
    )

    params = [date_from, date_to] + origin_ports + destination_ports
    cursor.execute(query, params)
    result = cursor.fetchall()
    return result
