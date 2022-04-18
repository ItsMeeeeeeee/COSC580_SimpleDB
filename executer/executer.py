from structure.table import DB_Table
import os 

class SQL_Executer:

    # put table inside the executer as dict
    def __init__(self, tables):
        self.tables = tables
    
    # add new table, still in dict
    def addTable(self, table, name):
        self.tables[name] = table
    
    def getTablesName(self):
        return self.tables.keys()
    
    
    def load():
        tables = {}
        path = 'save/'
        for path, _, file_list in os.walk(path):  
            for file_name in file_list:  
                tables[file_name] = DB_Table(file_name)
        return tables