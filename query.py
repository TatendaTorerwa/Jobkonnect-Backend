#!/usr/bin/env python3

import mysql.connector
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Establish a connection to your MySQL database
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()

# Define the ALTER TABLE query to add the new columns
alter_query = """
ALTER TABLE Users
ADD COLUMN company_name VARCHAR(100) NOT NULL,
ADD COLUMN website VARCHAR(255),
ADD COLUMN contact_info VARCHAR(255)
"""

# Execute the ALTER TABLE query
cursor.execute(alter_query)

# Commit the changes and close the connection
conn.commit()
conn.close()
