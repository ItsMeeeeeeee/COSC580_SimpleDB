from parser import SQLParser
from database import Table

class SQLExecuter:
    def __init__(self, tables):
        self.parser = SQLExecuter()
        self.tables = {}
        self._init_tables(tables)
        self.function = {
            'insert' : self._insert
        }
    
    def _init_tables(self, tables):
        for name, table in tables.items():
            self.tables[name] = table

    def execute(self, statement):
        action = self.parser.parse(statement)
        self.function[action['type']](action)

    def _insert(self, action):
        self.tables[action['table']].insert(action)