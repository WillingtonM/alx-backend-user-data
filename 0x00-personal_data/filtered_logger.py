#!/usr/bin/env python3
"""
    Module for handling Personal Data
"""
from typing import List
import re
import logging
from os import environ
import mysql.connector



PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
        Filters log line
    """
    for fld in fields:
        msg = re.sub(f'{fld}=.*?{separator}',
                         f'{fld}={redaction}{separator}', message)
    return msg


def get_logger() -> logging.Logger:
    """
        Returns a logging.Logger object
    """
    logg = logging.getLogger("user_data")
    logg.setLevel(logging.INFO)
    logg.propagate = False

    handle_stream = logging.StreamHandler()
    handle_stream.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logg.addHandler(handle_stream)

    return logg


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
        Creates connector to database
    """
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")

    db_conn = mysql.connector.connection.MySQLConnection(user=username,
                                                     password=password,
                                                     host=host,
                                                     database=db_name)
    return db_conn


def main():
    """
        Logs information about user records in table
    """
    db_conn = get_db()
    db_curs = db_conn.cursor()
    db_curs.execute("SELECT * FROM users;")
    field_names = [i[0] for i in db_curs.description]

    logger = get_logger()

    for row in db_curs:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    db_curs.close()
    db_conn.close()


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
        """ Filters values in incoming log records using filter_datum """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
