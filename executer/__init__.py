from parser import SQLParser

class SQLExecuter:
    def __init__(self):
        self.parser = SQLExecuter()
    
    def insert(self, statement):
        action = self.parser.parse(statement)
        if action['data'] == None:
            print()
        else:
            print()