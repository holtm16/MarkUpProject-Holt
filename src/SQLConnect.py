"""
Michael Holt
SQLConnect.py
The below code connects Python to SQL, handling HTML content appropriately.
"""


from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import HTMLScorer
        
class SQLConnect():
    DB_NAME = 'mark_up'
    TABLES = {}

    # Our constructor initializes the database and table.
    # The below function, whose entire structure was taken from
    # https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html,
    # initializes our database and the corresponding table 
    def __init__(self): 
        SQLConnect.TABLES['HTMLScores'] = (
            "CREATE TABLE `HTMLScores` ("
            "  `FileName` VARCHAR(50),"
            "  `Prefix` VARCHAR(10),"
            "  `Score` INT,"
            "  `DateRan` DATE,"
            "  `TimeRan` TIME,"
            "  PRIMARY KEY (`FileName`)"  # Make FileName the primary key since
                                          # they will be unique
            ") ")

        cnx = mysql.connector.connect(user='root')
        cursor = cnx.cursor()
        
        # Call a helper function to see if the database is successfully created
        self._create_database_helper(cursor)

        try:
            cnx.database = SQLConnect.DB_NAME    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                cnx.database = SQLConnect.DB_NAME
            else:
                print(err)
                exit(1)

        for name, ddl in SQLConnect.TABLES.iteritems():
            try:
                print("Creating table {}: ".format(name), end='')
                cursor.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        cursor.close()
        cnx.close()
        
    # The below function, also from https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html,
    # tries to create our database, quitting if unsuccessful
    def _create_database_helper(self, cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(SQLConnect.DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

    # insert_record takes an input filename, putting the corresponding record
    # into our table (does not function properly)
    def insert_record(self, fileName):
        HTMLObj = HTMLScorer.HTMLScorer(fileName)
        cnx = mysql.connector.connect(user='root', database=SQLConnect.DB_NAME)
        cursor = cnx.cursor()

        query = ("INSERT INTO `HTMLScores`"
                 "(Prefix, Score, DateRan, TimeRan)"
                 "VALUES"
                 "(%s, %s, %s, %s)")

        cursor.execute(query, (HTMLObj.getFilePrefix(), str(HTMLObj.scoreInput()), 'CURDATE()', 'CURTIME()'))

        cursor.close()
        cnx.close()
                        
                            
        
