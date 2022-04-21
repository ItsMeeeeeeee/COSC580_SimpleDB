#  coding = utf-8

import re


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
            'QUIT': self.__quit,
            'SHOW': self.__show,
            'DROP': self.__drop,
            'JOIN': self.__join,
        }
        self.__pattern_map = {
            'CREATE': r'(CREATE|create) (TABLE|table) (.*) \((.*)\)',
            'CREATE INDEX': r'(CREATE|create) (INDEX|index) (.*) (ON|on) (.*) \((.*)\)',
            'CREATE DATABASE': r'(CREATE|create) (DATABASE|database) (.*)',
            'SELECT': r'(SELECT|select) (.*) (FROM|from) (.*)',
            'UPDATE': r'(UPDATE|update) (.*) (SET|set) (.*)',
            'INSERT': r'(INSERT|insert) (INTO|into) (.*) \((.*)\) (VALUES|values) \((.*)\)',
            'INSERT_2': r'(INSERT|insert) (INTO|into) (.*) (VALUES|values) \((.*)\)'
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

        # 基于空格实现SQL语句的split，取出关键字
        base_statement = self.__filter_space(statement[0].split(" "))

        # SQL 语句一般由最少三个关键字组成，这里设定长度小于 2 时，又非退出等命令，则为错误语法
        if len(base_statement) < 2 and base_statement[0].lower() not in ['exit', 'quit', 'show']:
            print('Syntax Error for: %s' % statement)
            return

        # 在定义字典 __action_map 时，字典的键使用的是大写字符，此处转换为大写格式
        if "JOIN" in base_statement or "join" in base_statement:
            action_type = "JOIN"
        else:
            action_type = base_statement[0].upper()

        if action_type not in self.__action_map:
            print('Syntax Error for: %s' % statement)
            return

        # 根据字典得到对应的值
        # print('parse statement:',statement,action_type)
        action = self.__action_map[action_type](base_statement)
        # print('parse action:', action)

        if action is None or 'type' not in action:
            print('Syntax Error for: %s' % statement)
            return None

        conditions = []
        if len(statement) == 2:
            if 'and' in statement[1].lower():
                conditions_list = self.__filter_space(statement[1].split("AND"))
                action['condition_logic'] = 'AND'
                for cond in conditions_list:
                    conditions.extend(self.__filter_space(cond.split(" ")))
            elif 'or' in statement[1].lower():
                conditions_list = self.__filter_space(statement[1].split("OR"))
                action['condition_logic'] = 'OR'
                for cond in conditions_list:
                    conditions.extend(self.__filter_space(cond.split(" ")))
            else:
                conditions.extend(self.__filter_space(statement[1].split(" ")))

        if conditions:
            if len(conditions) < 3:
                print('Cannot Resolve Given Input!!!')
                return
            action['conditions'] = {}  # conditions 条件
            for index in range(0, len(conditions), 3):
                field = conditions[index]
                symbol = conditions[index + 1].upper()
                condition = conditions[index + 2]

                action['conditions'][field] = {
                    'operation': symbol,
                    'value': condition
                }
        return action

    def __get_comp(self, action):
        return re.compile(self.__pattern_map[action])

    # -----------------** 基于数据表的操作 **---------------------#
    def __join(self, statement):
        comp = self.__get_comp('SELECT')
        ret = comp.findall(' '.join(statement))[0]
        print(ret)
        if ret and len(ret) == 4:
            fields = ret[1]
            tables = []
            join_fields = []
            left = ret[3].split(" ")
            tables.append(left[0])
            tables.append(left[2])
            join_fields.append(left[-1])
            join_fields.append(left[-3])
            if fields != '*':
                fields = [field.strip() for field in fields.split(',')]
            return {
                'type': 'search join',
                'tables': tables,
                'fields': fields,
                'join fields': join_fields,
            }

    def __select(self, statement):
        # print('statement:', statement)
        comp = self.__get_comp('SELECT')
        ret = comp.findall(' '.join(statement))
        # print(ret, ' '.join(statement))
        if ret and len(ret[0]) == 4:
            fields = ret[0][1]
            table = ret[0][3]

            if fields != '*':
                fields = [field.strip() for field in fields.split(',')]
            return {
                'type': 'search',
                'table': table,
                'fields': fields
            }
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
                        value = int(value.strip())
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

    # 插入只支持"INSERT INTO 表名称 VALUES (值1, 值2,....)"
    def __insert(self, statement):
        comp = self.__get_comp('INSERT')
        ret = comp.findall(' '.join(statement))
        # print('parserSQL __insert ret:',ret)

        if ret and len(ret[0]) == 6:
            ret_tmp = ret[0]
            # check if the given table name is a string without space, raise error if do contain space
            if (len(ret_tmp[2].split(' ')) > 1):
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
            if (len(ret_tmp[2].split(' ')) > 1):
                return None
            values = ret_tmp[4].split(", ")
            data = {
                'type': 'insert',
                'table': ret_tmp[2],
                'values': values
            }
            return data

        return None

    # -----------------** 基于数据库的操作 **---------------------#
    # 选择使用的数据库
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
                'type': 'create db',
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
                'type': 'create index',
                'table': ret[0][4],
                'name': ret[0][2],
                'col': ret[0][5]
            }
            return info

        print("Cannot Resolve Given Input!!!")
        return None

    # 退出
    def __exit(self, _):
        return {
            'type': 'exit'
        }

    def __quit(self, _):
        return {
            'type': 'quit'
        }

    # 查看数据库列表或数据表 列表
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

    # 删除数据库或数据表
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
        print("ERROR!!! Cannot Resolve Given Input!")
        return


if __name__ == '__main__':
    d = SQLParser().parse(input(">"))
    print(f'tokens : {d}')
