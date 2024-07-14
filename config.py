#!/usr/bin/env python3

import os
Database configuration
"""
Database configuration

This script handles the configuration variables required for connecting to the database and other sensitive settings.

Variables:
- DB_USERNAME (str): The username for database authentication.
- DB_PASSWORD (str): The password for database authentication.
- DB_HOST (str): The host address of the database server.
- DB_PORT (str): The port number on which the database server is listening.
- DB_NAME (str): The name of the database to connect to.
- SECRET_KEY (str): A secret key used for cryptographic operations or application security.

These variables are populated from environment variables using os.getenv(), ensuring sensitive information like database credentials and secret keys are not hard-coded into the application source code.
"""
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')
