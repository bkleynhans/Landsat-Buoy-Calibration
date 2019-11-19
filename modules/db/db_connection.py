###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Database connection module
# Created By          : Benjamin Kleynhans
# Creation Date       : Autust 8, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 8, 2019
# Filename            : db_connection.py
#
###

import datetime
import mysql.connector
import settings
import time

from mysql.connector import errorcode


class Db_Connection:

    # Class Attributes
    db_user = settings.SQL_USER
    db_passwd = settings.SQL_PASSWORD
    db_server = settings.SQL_SERVER
    db_port = settings.SQL_PORT
    db_database = settings.SQL_DATABASE

    # Initializer / Instance Attributes
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.cnx = None

    # Connection information
    def db_connect(self):
        self.cnx = mysql.connector.connect(
                user=self.db_user,
                password=self.db_passwd,
                host=self.db_server,
                port=self.db_port,
                database=self.db_database)

        return self.cnx

    # Commit to database
    def db_commit(self):
        self.cnx.commit()

    # Open the database connection
    def open_connection(self):
        
        try:
            self.connection = self.db_connect()
            self.cursor = self.connection.cursor(buffered=True)
        except:
            self.cursor = "\n Unable to open database connection"

        return self.cursor

    # Close the database connection
    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    # Print current connection information
    def to_string(self):
        print("Database Server  : " + self.db_server)
        print("Database         : " + self.db_database)
        print("Database User    : " + self.db_user)
        print("Database Port    : " + self.db_port)

    # Test if the databse is available
    def db_available(self):
        
        db_status = False
        
        self.cursor = self.open_connection()

        #query = "SELECT * FROM MOCK_DATA WHERE last_name = 'Boyan'"
        query = "SELECT @@hostname"

        self.cursor.execute(query)

        count = 0

        for (hostname) in self.cursor:
            count += 1
            
        if count > 0:
            print("\n The database server is online\n")
            db_status = True
            
        else:
            print("\n!!! The database server appears to be offline !!!\n")
            input("Press Enter to continue...")

        self.close_connection()
        
        return db_status

