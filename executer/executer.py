from structure.table import DB_Table
from parser.sql_parser import Parser

import os 

class SQL_Executer:

    # put table inside the executer as dict
    def __init__(self, tables):
        self.parser = Parser()
        self.tables = tables
    
    # add new table, still in dict
    def addTable(self, table, name):
        self.tables[name] = table
    
    def getTablesName(self):
        return self.tables.keys()
    
    
    def execute(self, statement):
        self.parser.parse(statement)


    # load tables from the local file, each file represent a table, save it as dict
    def load():
        tables = {}
        path = 'save/'
        for path, _, file_list in os.walk(path):  
            for file_name in file_list:  
                tables[file_name] = DB_Table(file_name)
        return tables