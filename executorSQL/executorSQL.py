from parserSQL.parserSQL import SQLParser
from database.database import Table
from util.util import _print

import pickle
import os


class SQLExecuter:
    def __init__(self):
        # init the parserSQL
        self.parser = SQLParser()

        self.database = {}

        # init the dict to store each table and its' name
        # fill in the tables by using the given tables
        self.tables = None

        # map the keywords with function
        self.function = {
            'insert': self._insert,
            'create': self._create,
            'search' : self._select,
            'create index' : self._createIndex,
            'create db' : self._createDatabase,
            'use' : self._useDatabase,
            'exit' : self._exit,
            'show' : self._show
        }

        self._load()

    # execute the user entered statement
    def execute(self, statement):
        action = self.parser.parse(statement)
        if action:
            self.function[action['type']](action)

    # create table
    def _create(self, action):
        print(action)
        if self.tables == None:
            print("Did not Choose Database!")
            return 
        self.tables[action['name']] = Table(action['name'], action['cols'])

    # create index on specific table
    def _createIndex(self, action):
        print(action)
        if self.tables == None:
            print("Did not Choose Database!")
            return 
        self.tables[action['table']].createIndex(action)

    # insert data into sepcific table
    def _insert(self, action):
        print(action)
        if self.tables == None:
            print("Did not Choose Database!")
            return 
        self.tables[action['table']].insert(action)
        self.tables[action['table']].updateIndex()
    
    # get data from table
    def _select(self, action):
        print(action)
        if self.tables == None:
            print("Did not Choose Database!")
            return 
        res, type = self.tables[action['table']].select(action)
        self.tables[action['table']].updateIndex()
        _print(res, type)
    
    def _createDatabase(self, action):
        print(action)
        if action['name'] not in self.database.keys():
            self.database[action['name']] = {}
        else:
            print("Database %s Already Exists", action['name'])
    
    def _useDatabase(self, action):
        print(action)
        if action['database'] in self.database.keys():
            self.tables = self.database[action['database']]
        else:
            print("No Database Named %s", action['database'])
    
    def _show(self, action):
        print(action)
        if action['kind'] == 'databases':
            databases = list(self.database.keys())
            print(databases)
        else:
            if self.tables == None:
                print("Did not Choose Database!")
                return 
            tables = list(self.tables.keys())
            print(tables)


    def _exit(self, action):
        print(action)
        self._save()
        os._exit(0)

    def _load(self):
        db_path = "db"
        for path, db_list, _ in os.walk(db_path):  
            for db_name in db_list:  
                self.database[db_name] = {}
                for path, _, table_list in os.walk(os.path.join(path, db_name)):
                    for table_name in table_list:
                        f = open(os.path.join(path, table_name), 'rb')
                        self.database[db_name][table_name] = pickle.load(f)
                        f.close()
    def _save(self):
        path = "db"
        f = None
        for dname, tables in self.database.items():
            db_path = os.path.join(path, dname)
            if not os.path.exists(db_path):
                os.makedirs(db_path)
            for tname, table in tables.items():
                file_path = os.path.join(db_path, tname)
                f = open(file_path, 'wb')
                pickle.dump(table, f)
                f.close()