#  coding = utf-8

from ast import Sub
from re import compile
from tokenize import group


class SQLParser:
    def __init__(self):
        self.__action_map = {
            'SELECT': self.__select,
            'UPDATE': self.__update,
            'DELETE': self.__delete,
            'INSERT': self.__insert,
            'USE': self.__use,
            'CREATE': self.__create,
            'EXIT': self.__exit,
            'SHOW': self.__show,
            'DROP': self.__drop,
            'JOIN': self.__join,
        }
        self.__pattern_map = {
            'CREATE': r'(CREATE|create) (TABLE|table) (.*) \((.*)\)',
            'CREATE INDEX': r'(CREATE|create) (INDEX|index) (.*) (ON|on) (.*) \((.*)\)',
            'DROP INDEX': r'(DROP|drop) (INDEX|index) (.*) (ON|on) (.*)',
            'CREATE DATABASE': r'(CREATE|create) (DATABASE|database) (.*)',
            'SELECT': r'(SELECT|select) (.*) (FROM|from) (.*)',
            'UPDATE': r'(UPDATE|update) (.*) (SET|set) (.*)',
            'DELETE': r'(DELETE|delete) (FROM|from) (.*)',
            'INSERT': r'(INSERT|insert) (INTO|into) (.*) \((.*)\) (VALUES|values) \((.*)\)',
            'INSERT_2': r'(INSERT|insert) (INTO|into) (.*) (VALUES|values) \((.*)\)',
            'GROUPBY': r'(.*) (GROUP|group) (BY|by) (.*)'
        }

    def __filter_space(self, obj):
        ret = []
        for x in obj:
            if x.strip() == '' or x.strip() == 'AND':
                continue
            ret.append(x)
        return ret

    def parse(self, statement):
        if 'where' in statement:
            statement = statement.split("where")
        else:
            statement = statement.split("WHERE")

        base_statement = self.__filter_space(statement[0].split(" "))

        if len(base_statement) < 2 and base_statement[0].lower() not in ['exit', 'show']:
            print('Syntax Error for: %s' % statement)
            return

        if "JOIN" in base_statement or "join" in base_statement:
            action_type = "JOIN"
        else:
            action_type = base_statement[0].upper()

        if action_type not in self.__action_map:
            print('Syntax Error for: %s' % statement)
            return

        # print('parse statement:',statement,action_type)
        action = self.__action_map[action_type](base_statement)
        # print('parse action:', action)

        if action is None or 'type' not in action:
            print('Syntax Error for: %s' % statement)
            return None

        conditions = []
        if len(statement) == 2:
            if 'ORDER BY' in statement[1]:
                action['orderby'] = statement[1].split('ORDER BY')[1].strip().split(' ')[0]
                statement[1] = statement[1].replace('ORDER BY ' + action['orderby'], '')
            elif 'order by' in statement[1]:
                action['orderby'] = statement[1].split('order by')[1].strip().split(' ')[0]
                statement[1] = statement[1].replace('ORDER BY ' + action['orderby'], '')
            if 'GROUP BY' in statement[1]:
                sub_statement = statement[1].split('GROUP BY')
            else:
                sub_statement = statement[1].split('group by')
            if len(sub_statement) > 1:
                if 'limit' in sub_statement[1]:
                    sub_sub_statement = sub_statement[1].split('limit')
                else:
                    sub_sub_statement = sub_statement[1].split('LIMIT')
                if len(sub_sub_statement) == 1:
                    action['groupby'] = sub_statement[1].strip()
                else:
                    action['groupby'] = sub_sub_statement[0].strip()
                    action['limit'] = sub_sub_statement[1].strip()
            else:
                if 'LIMIT' in sub_statement[0]:
                    action['limit'] = sub_statement[0].split('LIMIT')[1].strip().split(' ')[0]
                    sub_statement[0] = sub_statement[0].replace('LIMIT ' + action['limit'], '')
                elif 'limit' in sub_statement[0]:
                    action['limit'] = sub_statement[0].split('limit')[1].strip().split(' ')[0]
                    sub_statement[0] = sub_statement[0].replace('limit ' + action['limit'], '')

            if 'and' in sub_statement[0].lower():
                conditions_list = self.__filter_space(sub_statement[0].split("AND"))
                action['condition_logic'] = 'AND'
                for cond in conditions_list:
                    conditions.extend(self.__filter_space(cond.split(" ")))
            elif 'or' in sub_statement[0].lower():
                conditions_list = self.__filter_space(sub_statement[0].split("OR"))
                action['condition_logic'] = 'OR'
                for cond in conditions_list:
                    conditions.extend(self.__filter_space(cond.split(" ")))
            else:
                conditions.extend(self.__filter_space(sub_statement[0].split(" ")))

        if conditions:
            if len(conditions) < 3:
                print('Cannot Resolve Given Input!!!')
                return
            action['conditions'] = []  # conditions ??????
            for index in range(0, len(conditions), 3):
                field = conditions[index]
                symbol = conditions[index + 1].upper()
                condition = conditions[index + 2]

                # action['conditions'][field] = {
                #     'operation': symbol,
                #     'value': condition
                # }
                action['conditions'].append({
                    'field': field,
                    "cond": {
                        'operation': symbol,
                        'value': condition
                    }
                })
        return action

    def __get_comp(self, action):
        return compile(self.__pattern_map[action])

    def __join(self, statement):
        comp = self.__get_comp('SELECT')
        ret = comp.findall(' '.join(statement))[0]
        # print(ret)
        if ret and len(ret) == 4:
            fields = ret[1]
            join_fields = {}
            left = ret[3].split(" ")
            join_field = [left[-1], left[-3]]
            for str in join_field:
                table = str.split(".")[0]
                col = str.split(".")[1]
                join_fields[table] = col
            if fields != '*':
                fields = [field.strip() for field in fields.split(',')]
            return {
                'type': 'search join',
                'join type': left[1],
                'tables': left[0],
                'fields': fields,
                'join fields': join_fields,
            }

    def __select(self, statement):
        comp = self.__get_comp('SELECT')
        ret = comp.findall(' '.join(statement))
        # print(ret, ' '.join(statement))
        if ret and len(ret[0]) == 4:
            comp = self.__get_comp('GROUPBY')
            groupby = comp.findall(ret[0][3])

            fields = ret[0][1]
            if fields != '*':
                fields = [field.strip() for field in fields.split(',')]

            action = {
                'type': 'search',
                'fields': fields
            }

            if groupby:
                action['table'] = groupby[0][0]
                action['groupby'] = groupby[0][3]

            if 'ORDER' in statement:
                index = statement.index('BY')
                action['orderby'] = statement[index + 1]
            elif 'order' in statement:
                index = statement.index('by')
                action['orderby'] = statement[index + 1]
            try:
                if 'limit' in ret[0][3]:
                    action['limit'] = int(ret[0][3].split('LIMIT')[1].split('order by')[0].split('ORDER BY')[0].strip())
                    action['table'] = ret[0][3].split('limit')[0].split('order by')[0].split('ORDER BY')[0].strip()
                elif 'LIMIT' in ret[0][3]:
                    action['limit'] = int(ret[0][3].split('LIMIT')[1].split('order by')[0].split('ORDER BY')[0].strip())
                    action['table'] = ret[0][3].split('LIMIT')[0].split('order by')[0].split('ORDER BY')[0].strip()
                else:
                    action['table'] = ret[0][3].split(' ')[0]
            except Exception:
                print("Please Provide Integer as LIMIT Constraint!!!")

            return action
        return None

    def __update(self, statement):
        comp = self.__get_comp('UPDATE')
        ret = comp.findall(' '.join(statement))

        if ret and len(ret[0]) == 4:
            data = {
                'type': 'update',
                'table': ret[0][1],
                'data': {}
            }
            set_statement = ret[0][3].split(',')
            for s in set_statement:
                s = s.split('=')
                field = s[0].strip()
                value = s[1].strip()
                if "'" in value or '"' in value:
                    value = value.replace('"', '').replace(",", '').strip()
                else:
                    try:
                        value = value.strip()
                    except:
                        return None
                data['data'][field] = value
            return data
        return None

    def __delete(self, statement):
        return {
            'type': 'delete',
            'table': statement[2]
        }

    def __insert(self, statement):
        comp = self.__get_comp('INSERT')
        ret = comp.findall(' '.join(statement))
        # print('parserSQL __insert ret:',ret)

        if ret and len(ret[0]) == 6:
            ret_tmp = ret[0]
            # check if the given table name is a string without space, raise error if do contain space
            if len(ret_tmp[2].split(' ')) > 1:
                return None
            data = {
                'type': 'insert',
                'table': ret_tmp[2],
                'data': {}
            }
            fields = ret_tmp[3].split(",")
            values = ret_tmp[5].split(",")
            print('parserSQL __insert fields:', fields)

            for i in range(0, len(fields)):
                field = fields[i]
                value = values[i]
                if "'" in value or '"' in value:
                    value = value.replace('"', '').replace("'", '').strip()
                else:
                    try:
                        value = int(value.strip())
                    except:
                        return None
                data['data'][field] = value
            return data

        ret = self.__get_comp('INSERT_2').findall(' '.join(statement))
        if ret and len(ret[0]) == 5:
            ret_tmp = ret[0]
            # check if the given table name is a string without space, raise error if do contain space
            if len(ret_tmp[2].split(' ')) > 1:
                return None
            values = ret_tmp[4].split(", ")
            data = {
                'type': 'insert',
                'table': ret_tmp[2],
                'values': values
            }
            return data

        return None

    def __use(self, statement):
        return {
            'type': 'use',
            'database': statement[1]
        }

    def __create(self, statement):
        comp = self.__get_comp('CREATE DATABASE')
        ret = comp.findall(' '.join(statement))
        if ret:
            info = {
                'type': 'create_db',
                'name': ret[0][2]
            }
            return info

        comp = self.__get_comp('CREATE')
        ret = comp.findall(' '.join(statement))
        # check if the values and definition is provided
        if ret:
            info = {}
            # set the tend first
            info['type'] = 'create'
            info['name'] = statement[2]
            info['cols'] = {}
            # extract the var name and its' type
            vars = ret[0][3].split(',')
            for var_type in vars:
                detailed = var_type.strip().split(' ')
                info['cols'][detailed[0]] = []
                for i in range(1, len(detailed)):
                    info['cols'][detailed[0]].append(detailed[i])
            return info

        comp = self.__get_comp('CREATE INDEX')
        ret = comp.findall(' '.join(statement))
        if ret:
            info = {
                'type': 'create_index',
                'table': ret[0][4],
                'name': ret[0][2],
                'col': ret[0][5]
            }
            return info

        print("Cannot Resolve Given Input!!!")
        return None

    def __exit(self, _):
        return {
            'type': 'exit'
        }

    def __show(self, statement):
        kind = statement[1]

        if kind.upper() == 'DATABASES':
            return {
                'type': 'show',
                'kind': 'databases'
            }
        if kind.upper() == 'TABLES':
            return {
                'type': 'show',
                'kind': 'tables'
            }

    def __drop(self, statement):
        kind = statement[1]
        if len(statement) < 3:
            print("ERROR!!! Cannot Resolve Given Input!")
            return
        elif kind.upper() == 'DATABASE':
            return {
                'type': 'drop',
                'kind': 'database',
                'name': statement[2]
            }
        elif kind.upper() == 'TABLE':
            return {
                'type': 'drop',
                'kind': 'table',
                'name': statement[2]
            }
        elif kind.upper() == 'INDEX':
            comp = self.__get_comp('DROP INDEX')
            ret = comp.findall(' '.join(statement))
            if ret:
                return {
                    'type': 'drop',
                    'kind': 'index',
                    'name': statement[2],
                    'table': ret[0][4]
                }
        print("ERROR!!! Cannot Resolve Given Input!")
        return

