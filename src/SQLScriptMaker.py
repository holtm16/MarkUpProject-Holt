"""
Michael Holt
SQLScriptMaker.py
The below code outputs the appropriate SQL commands to a text file called
ShellScript.txt within the schema folder.
"""

import HTMLScorer

class SQLScriptMaker():    
    # Our constructor puts the text necessary to create a table into our
    # output attribute
    def __init__(self):
        self._output =  "-- Creating our table HTMLScores\n" + \
                        "CREATE TABLE HTMLScores \n" + \
                        "(\n" + \
                        "\tInputId INT AUTO_INCREMENT,\n" + \
                        "\tFileName VARCHAR(50),\n" + \
                        "\tPrefix VARCHAR(10),\n" + \
                        "\tScore INT,\n" + \
                        "\tDateRan DATE,\n" + \
                        "\tTimeRan TIME,\n" + \
                        "\tPRIMARY KEY (InputId)\n" + \
                        ");\n\n"
                        
    # insert_record takes an input filename and inserts the corresponding record into our table
    def insert_record(self, fileName):
        HTMLObj = HTMLScorer.HTMLScorer(fileName)
        insertQuery = "-- Inserting a new record into the table HTMLScores\n" + \
                      "INSERT INTO HTMLScores \n" + \
                      "\t(FileName, Prefix, Score, DateRan, TimeRan)\n" + \
                      "VALUES \n" + \
                      "\t('" + fileName + "', '" + HTMLObj.getFilePrefix() + "', " +\
                      str(HTMLObj.scoreInput()) + ", CURDATE(), CURTIME());\n\n"
        self._output += insertQuery
        
    # retrieve_unique_id_scores adds a query to get all records with the input id
    def retrieve_unique_id_scores(self, uniqueId):
        query = "-- Retrieving all scores for a given id (prefix)\n" + \
                "SELECT * FROM HTMLScores \n" + \
                "WHERE Prefix = '" + uniqueId + "';\n\n"
        self._output += query

    # retrieve_all_scores_in_date_range adds a query to get all the records run within a given date range,
    # where an input date is of the form "YYYY_MM_DD"
    def retrieve_all_scores_in_date_range(self, startDate, endDate):
        query = "-- Retrieving all scores in a date range\n" + \
                "SELECT * FROM HTMLScores \n" + \
                "WHERE DateRan >= '" + startDate + "' AND DateRan <= '" + endDate + "';\n\n"
        self._output += query

    # retrieve_highest_score_for_id takes an input id, adding a query to find the highest score
    # with the corresponding id
    def retrieve_highest_score_for_id(self, uniqueId):
        query = "-- Retrieving the highest score for a given id (prefix)\n" + \
                "SELECT Prefix, MAX(Score) FROM HTMLScores \n" + \
                "WHERE Prefix = '" + uniqueId + "';\n\n"
        self._output += query

    # retrieve_lowest_score_for_id takes an input id, adding a query to find the lowest score
    # with the corresponding id
    def retrieve_lowest_score_for_id(self, uniqueId):
        query = "-- Retrieving the lowest score for a given id (prefix)\n" + \
                "SELECT Prefix, MIN(Score) FROM HTMLScores \n" + \
                "WHERE Prefix = '" + uniqueId + "';\n\n"
        self._output += query

    # find_avg_for_all_runs takes an input id, adding a query to find the average score across
    # all runs for all ids (prefixes)
    def find_avg_for_all_runs(self):
        query = "-- Finding the average score for all ids (prefixes)\n" + \
                "SELECT Prefix, AVG(Score) AS avgScore FROM HTMLScores\n" + \
                "GROUP BY Prefix;\n\n"
        self._output += query

    # automate_data_insertion adds queries to insert all the provided data files into the table
    def automate_data_insertion(self):
        listOfHTMLFiles = ["bob_2013_02_10.html", "bob_2013_02_15.html","bob_2013_03_01.html", \
                           "cari_2013_02_15.html", "cari_2013_02_16.html", "cari_2013_03_05.html", \
                           "john_2013_01_05.html", "john_2013_02_13.html", "john_2013_03_13.html"]
        for HTMLFile in listOfHTMLFiles:
            self.insert_record(HTMLFile)

    # write_to_out writes all the previous text accumulated from running methods within this class
    # to a text file in the schema folder called "SQLScript.txt"
    def write_to_out(self):
        textOutput = open('../schema/SQLScript.txt', 'w')
        textOutput.write(self._output)
        textOutput.close()

        



