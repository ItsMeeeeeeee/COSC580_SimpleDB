from parserSQL.parserSQL import SQLParser
from database.database import Table
from util.util import _print, merge_dict, merge_result_inner

from shutil import rmtree
from pickle import dump, load
import os
import copy


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
            'search': self._select,
            'delete': self._delete,
            'update': self._update,
            'create_index': self._createIndex,
            'create_db': self._createDatabase,
            'use': self._useDatabase,
            'exit': self._exit,
            'show': self._show,
            'drop': self._drop,
            'search join': self._select_join,
        }

        self._load()

    # exit to exit
    def run(self):
        while True:
            statement = input("sdb> ")
            self.execute(statement)

    # execute the user entered statement
    def execute(self, statement):
        try:
            action = self.parser.parse(statement)
            if action:
                self.function[action['type']](action)
        except Exception:
            print("ERROR!!! Cannot Resolve The Given Input!!")


    # create table
    def _create(self, action):
        # print(action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return
        try:
            if action['name'] in self.tables.keys():
                print("Table %s Already Exists!" % (action['name']))
                return
            self.tables[action['name']] = Table(action['name'], action['cols'])
            self._updateTable({
                'database': self.currentDB,
                'name': action['name']
            })
        except Exception as e:
            print(e.args[0])
        

    # create index on specific table
    def _createIndex(self, action):
        # print(action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return
        self.tables[action['table']].createIndex(action)
        self._updateTable({
            'database': self.currentDB,
            'name': action['table']
        })

    # insert data into sepcific table
    def _insert(self, action):
        # print(action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return
        if self.tables.get(action['table']) == None:
            print("ERROR！！！ No Table Named %s" % (action['table']))
        else:
            try:
                self.tables[action['table']].insert(action)
                self.tables[action['table']].updateIndex()
                self._updateTable({
                    'database': self.currentDB,
                    'name': action['table']
                })
            except Exception as e:
                print(e.args[0])

    # get data from table
    def _select(self, action):
        # print(action)
        if self.currentDB == None:
            print("Did not Choose Database!")
            return
        try:
            if action['table'] not in self.tables.keys():
                print('Error!!! No Table Named %s' % (action['table']))
                return
            res, type, orderby = self.tables[action['table']].select(action)
            
            if orderby:
                for key, value in res.items():
                    new_value = copy.deepcopy(value)
                    new_value = [i for _,i in sorted(zip(orderby, new_value))]
                    res[key] = new_value
            
            if action.get('limit'):
                _print(res, type, action['limit'])
            else:
                _print(res, type)
        except Exception as e:
            print(e.args[0])
        # print(f"res {res}")
        # print(f"type {type}")

    def _select_join(self, action):
        """
        :param action: {'type': 'search join',
                        'tables': ['TABLE1', 'TABLE2'],
                        'fields': '*',
                        'join fields': {'TABLE2':'COL2', 'TABLE1':'COL2'},
                        'conditions': [{'field': 'TABLE1.COL1', 'cond': {'operation': '=', 'value': 'YES'}}]}
        :return: print result
        """
        # print(f"Now using join SQL!", action)
        if self.currentDB is None:
            print("Did not Choose Database!")
            return
        # first we need to get first tables data
        if action.get("conditions"):
            first_table = action['conditions'][0]['field'].split(".")[0]
            first_table_cond_field = action['conditions'][0]['field'].split(".")[1]
            first_table_col = action['join fields'][first_table]
            action_to_table1 = {
                'type': 'search',
                'table': first_table,
                'fields': action['fields'],
                'conditions': [{
                    'field': first_table_cond_field,
                    'cond': action['conditions'][0]['cond'],
                }]
            }
        else:
            first_table = list(action['join fields'].keys())[0]
            first_table_col = action['join fields'][first_table]
            action_to_table1 = {
                'type': 'search',
                'table': first_table,
                'fields': action['fields'],
            }
        # print('read table1')
        res1, type1 = self.tables[first_table].select(action_to_table1)
        # print(res1)
        # use join fields to search table2 based on the values we select in table1
        for k, v in action['join fields'].items():
            if k != first_table:
                second_table_field = v
                second_table = k
        conditions = []
        for index in res1[first_table_col]:
            condition = {
                'field': second_table_field,
                "cond": {
                    'operation': '=',
                    'value': f'{index}',
                }
            }
            conditions.append(condition)

        action_to_table2 = {
            'type': 'search',
            'table': [action['tables'][1]],
            'condition_logic': 'OR',
            'fields': action['fields'],
            'conditions': conditions
        }
        # print("read table 2")
        res2, type2 = self.tables[second_table].select(action_to_table2)
        # print(res2)
        result = {}
        types = {}
        result = merge_result_inner(result, res1, res2, first_table_col, second_table_field)
        types = merge_dict(types, type1)
        merge_dict(types, type2)

        _print(result, types)

    def _delete(self, action):
        # print(action)
        if self.currentDB is None:
            print("Did not Choose Database!")
            return
        if action['table'] not in self.tables.keys():
            print("No Table Named %s" % (action['table'].strip()))
            return
        self.tables[action['table']].delete(action)
        self.tables[action['table']].updateIndex()
        self._updateTable({
            'database': self.currentDB,
            'name': action['table']
        })

    def _update(self, action):
        try:
            if action['table'] not in self.tables.keys():
                print(f"Not such table: {action['table']}")
                return

            if self.currentDB is None:
                print("Did not Choose Database!")
                return
            self.tables[action['table']].update(action)
            self.tables[action['table']].updateIndex()
            self._updateTable({
                'database': self.currentDB,
                'name': action['table']
            })
        except Exception as e:
            print(e.args[0])

    def _createDatabase(self, action):
        # print(action)
        if action['name'] not in self.database.keys():
            self.database[action['name']] = {}
            db_path = os.path.join('db', action['name'])
            if not os.path.exists(db_path):
                os.makedirs(db_path)
        else:
            print("Database '%s' Already Exists" % (action['name']))

    def _useDatabase(self, action):
        # print(action)
        if action['database'] in self.database.keys():
            self.currentDB = action['database']
            self.tables = self.database[action['database']]
        else:
            print("No Database Named %s" % (action['database']))

    def _show(self, action):
        # print(action)
        if action['kind'] == 'databases':
            databases = list(self.database.keys())
            # print(databases)
            _print({
                'databases' : databases
            })
        else:
            if self.currentDB == None:
                print("Did not Choose Database!")
                return
            tables = list(self.tables.keys())
            _print({
                'tables' : tables
            })
            # print(tables)

    def _drop(self, action):
        # print(action)
        if action['kind'] == 'database':
            if action['name'] not in self.database.keys():
                print("No Database Named %s", action['name'])
                return
            self._dropDB(action)
            del self.database[action['name']]
            if self.currentDB == action['name']:
                self.currentDB = None
        elif action['kind'] == 'table':
            if self.currentDB == None:
                print("Did not Choose Database!")
                return
            if action['name'] not in self.tables.keys():
                print("No Table Named %s", action['name'])
                return
            action['database'] = self.currentDB
            self._dropTable(action)
            del self.database[self.currentDB][action['name']]
            self.tables = self.database[self.currentDB]
        elif action['kind'] == 'index':
            if self.currentDB == None:
                print("Did not Choose Database!")
                return
            if action['table'] not in self.tables.keys():
                print("No Table Named %s", action['table'])
                return 
            self.tables[action['table']].dropIndex(action)

    def _dropDB(self, action):
        # print(action)
        folderpath = os.path.join("db", action['name'])
        rmtree(folderpath)

    def _dropTable(self, action):
        # print(action)
        filepath = os.path.join("db", action['database'])
        filepath = os.path.join(filepath, action['name'])
        os.remove(filepath)

    def _updateTable(self, action):
        # print(action)
        filepath = os.path.join("db", action['database'])
        filepath = os.path.join(filepath, action['name'])
        if os.path.exists(filepath):
            os.remove(filepath)
        f = open(filepath, 'wb')
        dump(self.tables[action['name']], f)
        f.close()

    def _exit(self, action):
        # print(action)
        self._save()
        os._exit(0)

    def _load(self):
        db_path = "db"
        for path, db_list, _ in os.walk(db_path):
            for db_name in db_list:
                self.database[db_name] = {}
                for filepath, _, table_list in os.walk(os.path.join(path, db_name)):
                    for table_name in table_list:
                        f = open(os.path.join(filepath, table_name), 'rb')
                        self.database[db_name][table_name] = load(f)
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
                dump(table, f)
                f.close()
