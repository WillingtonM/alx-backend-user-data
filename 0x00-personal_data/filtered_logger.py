#!/usr/bin/env python3
"""
    Module for handling Personal Data
"""
import re
from typing import List
import logging
import mysql.connector
import os

PII_FIELDS = ("name", "email", "password", "ssn", "phone")


class RedactingFormatter(logging.Formatter):
    """
        The Redacting Formatter class
    """

    SEPARATOR = ";"
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            formats a LogRecord
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """
        Creates connector to database
    """
    conn_db = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return conn_db


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
        Filters log line
    """
    for fld in fields:
        msg = re.sub(f'{fld}=(.*?){separator}',
                     f'{fld}={redaction}{separator}', message)
    return msg


def get_logger() -> logging.Logger:
    """
        Returns a logging.Logger object
    """
    logg = logging.getLogger("user_data")
    handle_stream = logging.StreamHandler()
    handle_stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logg.setLevel(logging.INFO)
    logg.propagate = False
    logg.addHandler(handle_stream)
    return logg


def main() -> None:
    """
        Logs information about user records in table
    """
    db_conn = get_db()
    db_curs = db_conn.cursor()
    db_curs.execute("SELECT * FROM users;")

    heads = [field[0] for field in db_curs.description]
    loggr = get_logger()

    for row in db_curs:
        info_answer = ''
        for f, p in zip(row, heads):
            info_answer += f'{p}={(f)}; '
        loggr.info(info_answer)

    db_curs.close()
    db_conn.close()


if __name__ == '__main__':
    main()
