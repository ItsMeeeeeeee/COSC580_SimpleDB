from parserSQL.parserSQL import SQLParser
from database.database import Table
from util.util import _print

import shutil
import pickle
import os


class SQLExecuter:
    def __init__(self):
        # init the parserSQL
        self.parser = SQLParser()

        self.database = {}
        self.currentDB = None

        # init the dict to store each table and its' name
        # fill in the tables by using the given tables
        self.tables = None

        # map the keywords with function
        self.function = {
            'insert': self._insert,
            'create': self._create,
            'search' : self._select,
            'delete' : self._delete,
            'create index' : self._createIndex,
            'create db' : self._createDatabase,
            'use' : self._useDatabase,
            'exit' : self._exit,
            'show' : self._show,
            'drop' : self._drop,
            'search join': self._select_join,
        }

        self._load()
    # TODO exit to exit
    def run(self):
        while True:
            statement = input("sdb> ")
            self.execute(statement)


    # execute the user entered statement
    def execute(self, statement):
        action = self.parser.parse(statement)
        if action:
            self.function[action['type']](action)

    # create table
    def _create(self, action):
        print(action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return 
        self.tables[action['name']] = Table(action['name'], action['cols'])
        self._updateTable({
            'database' : self.currentDB,
            'name' : action['name']
        })

    # create index on specific table
    def _createIndex(self, action):
        print(action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return 
        self.tables[action['table']].createIndex(action)
        self._updateTable({
            'database' : self.currentDB,
            'name' : action['table']
        })

    # insert data into sepcific table
    def _insert(self, action):
        print(action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return 
        self.tables[action['table']].insert(action)
        self.tables[action['table']].updateIndex()
        self._updateTable({
            'database' : self.currentDB,
            'name' : action['table']
        })
    
    # get data from table
    def _select(self, action):
        print(action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return 
        res, type = self.tables[action['table']].select(action)
        self.tables[action['table']].updateIndex()
        _print(res, type)

    def _select_join(self, action):
        print(f"Now using join SQL!", action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return
        # first we need to get first tables data
        action_to_table1 = {
            'type': 'search',
            'table': [action['tables'][0]],
            'fields': action['fields'],
            'conditions': action['conditions']
        }
        res1, type1 = self.tables[action['tables'][0]].select(action_to_table1)
        # use join fields to search table2 based on the values we select in table1
        action_to_table2 = {
            'type': 'search',
            'table': [action['tables'][1]],
            'condition_logic': 'AND',
            'fields': action['fields'],
            'conditions': action['conditions']
        }
        actions = {
            'type': 'search',
            'table': 'TABLE1',
            'fields': '*',
            'condition_logic': 'AND',
            'conditions': {
                'COL2': {
                    'operation': '=',
                    'value': '1'
                },
            'COL1': {
                'operation': '=',
                'value': 'YES'}
            }
        }
        # self.tables[action['tables'][1]].
        print(res1)
        print(type1)
        # {'COL1': ['YES', 'YES', 'YES', 'No', 'YES', 'YES', 'YES', 'No', 'YES'],
        #  'COL2': [7, 6, 4, 9, 11, 15, 18, 19, 19]}
        # {'COL1': ['Boolean'], 'COL2': ['int']}
        _print(res1, type1)
    
    def _delete(self, action):
        print(action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return 
        self.tables[action['table']].delete(action)
        self.tables[action['table']].updateIndex()
        self._updateTable({
            'database' : self.currentDB,
            'name' : action['table']
        })

    def _createDatabase(self, action):
        print(action)
        if action['name'] not in self.database.keys():
            self.database[action['name']] = {}
        else:
            print("Database %s Already Exists", action['name'])
    
    def _useDatabase(self, action):
        print(action)
        if action['database'] in self.database.keys():
            self.currentDB = action['database']
            self.tables = self.database[action['database']]
        else:
            print("No Database Named %s", action['database'])
    
    def _show(self, action):
        print(action)
        if action['kind'] == 'databases':
            databases = list(self.database.keys())
            print(databases)
        else:
            if self.currentDB == None:
                print("Did not Choose Database!")
                return 
            tables = list(self.tables.keys())
            print(tables)

    def _drop(self, action):
        # print(action)
        if action['kind'] == 'database':
            if action['name'] not in self.database.keys():
                print("No Database Named %s", action['name'])
            self._dropDB(action)
            del self.database[action['name']]
            if self.currentDB == action['name']:
                self.currentDB = None
        else:
            if self.currentDB == None:
                print("Did not Choose Database!")
                return 
            if action['name'] not in self.tables.keys():
                print("No Table Named %s", action['name'])
            action['database'] = self.currentDB
            self._dropTable(action)
            del self.database[self.currentDB][action['name']]
            self.tables = self.database[self.currentDB]
    def _dropDB(self, action):
        print(action)
        folderpath = os.path.join("db", action['name'])
        shutil.rmtree(folderpath)
    def _dropTable(self, action):
        print(action)
        filepath = os.path.join("db", action['database'])
        filepath = os.path.join(filepath, action['name'])
        os.remove(filepath)
    def _updateTable(self, action):
        print(action)
        filepath = os.path.join("db", action['database'])
        filepath = os.path.join(filepath, action['name'])
        if os.path.exists(filepath):
            os.remove(filepath)
        f = open(filepath, 'wb')
        pickle.dump(self.tables[action['name']], f)
        f.close()

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

    def _save(self, table):
        path = "db"
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