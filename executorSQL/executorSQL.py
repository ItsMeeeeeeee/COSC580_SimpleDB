from parserSQL.parserSQL import SQLParser
from database.database import Table
from util.util import _print


class SQLExecuter:
    def __init__(self, tables={}):
        # init the parserSQL
        self.parser = SQLParser()

        # init the dict to store each table and its' name
        # fill in the tables by using the given tables
        self.tables = tables

        # map the keywords with function
        self.function = {
            'insert': self._insert,
            'create': self._create,
            'search' : self._select,
            'create index' : self._createIndex
        }

    def execute(self, statement):
        action = self.parser.parse(statement)
        if action:
            self.function[action['type']](action)

    def _insert(self, action):
        print(action)
        self.tables[action['table']].insert(action)

    def _create(self, action):
        print(action)
        self.tables[action['name']] = Table(action['name'], action['cols'])
    
    def _select(self, action):
        print(action)
        res, type = self.tables[action['table']].select(action)
        _print(res, type)
    
    def _createIndex(self, action):
        print(action)
        self.tables[action['table']].createIndex(action)