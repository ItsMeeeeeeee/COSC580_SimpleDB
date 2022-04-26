from operator import index
from util import util
from bplus_tree import BPlusTree
from re import findall


class Table:
    # {
    # 'col1' : ['string', 'unique'],
    # 'col2' : ['int', 'primary key']
    # }
    def __init__(self, name, var_type):
        # table anme
        self.name = name
        # all columns' name
        self.var = []
        # all columns' corresponding variable type and constraint
        self.type = []
        # a dictionary of list, that used to store each columns' data
        self.data = {}
        # btrees dictionary for create index
        self.btrees = {}

        self._condition_map = {
            '=': self._equal,
            '>': self._bigger,
            '<': self._smaller,
            '>=': self._biggerAndEqual,
            '<=': self._smallerAndEqual,
        }

        self._select_filter_map = {
            'avg': self._select_avg,
            'count': self._select_count,
            'max': self._select_max,
            'min': self._select_min,
            'sum': self._select_sum,
        }

        # self defined index, used if no primary key given
        self.index = 0

        # save each columns' name and type to self
        self._init_var_type(var_type)
        # check if the given columns include the primary key, use '__index__' as the primary key if not provided
        self.primary = self._checkPrimary()

        # init the list for each columns
        for col in self.var:
            self.data[col] = []

        # if primary key provided, this line is just overwrite the previous step; if not, this line will create a new list(key pair in the dictionary)
        self.data[self.primary] = []

    # the helper function help condiction
    def _filter(self, cond, col):
        try:
            return self._condition_map[cond["operation"]](cond, col)
        except Exception:
            print('Error! Cannot Resolve Given Input')
            return

    def _format(self, col, value):
        if self.type[self.var.index(col)][0] == 'int':
            return int(value)
        elif self.type[self.var.index(col)][0] == 'float':
            return float(value)
        return value

    def _equal(self, cond, col):
        if col in self.btrees.keys():
            indexs = self.btrees[col]['tree'].search('=', self._format(col, cond["value"]))
            return indexs
        return util.get_equal_keys_list(self.data[col], self._format(col, cond["value"]))

    def _bigger(self, cond, col):
        if col in self.btrees.keys():
            indexs = self.btrees[col]['tree'].search('>', self._format(col, cond["value"]))
            return indexs
        return util.get_more_keys_list(self.data[col], self._format(col, cond["value"]))

    def _smaller(self, cond, col):
        if col in self.btrees.keys():
            indexs = self.btrees[col]['tree'].search('<', self._format(col, cond["value"]))
            return indexs
        return util.get_less_keys_list(self.data[col], self._format(col, cond["value"]))

    def _biggerAndEqual(self, cond, col):
        if col in self.btrees.keys():
            indexs = self.btrees[col]['tree'].search('>=', self._format(col, cond["value"]))
            return indexs
        return util.get_more_equal_keys_list(self.data[col], self._format(col, cond["value"]))

    def _smallerAndEqual(self, cond, col):
        if col in self.btrees.keys():
            indexs = self.btrees[col]['tree'].search('<=', self._format(col, cond["value"]))
            return indexs
        return util.get_less_equal_keys_list(self.data[col], self._format(col, cond["value"]))
        # return [index for index, v in enumerate(self.data[col]) if v <= float(cond["value"])]

    # update index btree after each operation
    def updateIndex(self):
        if self.btrees == {}:
            return
        for name in self.btrees.keys():
            self.btrees[name]['tree'] = BPlusTree()
            for i in range(len(self.data[name])):
                self.btrees[name]['tree'].insert(self.data[name][i], i)

    # save each columns' name and type to self
    def _init_var_type(self, var_type):
        for var, type in var_type.items():
            self.var.append(var)
            self.type.append(type)

    # check if primary key is provided
    def _checkPrimary(self):
        primary = 'index__'
        for key, type in zip(self.var, self.type):
            if 'primary' in type:
                if primary == 'index__':
                    primary = key
                else:
                    raise Exception("ERROR! Duplicate Primary Key Set!!!")
        return primary

    def _delete_data(self, index_delete):
        # sort the index list in decending order so we can remove all in once without error
        index_delete.sort(reverse=True)
        for index in index_delete:
            for col in self.var:
                del self.data[col][index]
            if self.primary == 'index__':
                del self.data[self.primary][index]

    ########################################################################################################
    def _select_avg(self, field, index):
        _sum = 0
        for i in index:
            _sum += self.data[field][i]

        return [_sum / len(index)]

    def _select_count(self, field, index):
        return [len(index)]

    def _select_max(self, field, index):
        _max = self.data[field][index[0]]
        for i in index:
            if _max < self.data[field][i]:
                _max = self.data[field][i]
        return [_max]

    def _select_min(self, field, index):
        _min = self.data[field][index[0]]
        for i in index:
            if _min > self.data[field][i]:
                _min = self.data[field][i]

        return [_min]

    def _select_sum(self, field, index):
        _sum = 0
        for i in index:
            _sum += self.data[field][i]
        print(_sum)
        return [_sum]

    # a helper function used to help select function to get corresponding info
    def _select_data(self, index_select, fields):
        try:
            result = dict()
            for index in index_select:
                for field in fields:
                    if not result.get(field, False):
                        result[field] = []
                    result[field].append(self.data[field][index])
            return result
        except Exception:
            print("key error!")

    def _select_data_3(self, index_select, fields, filter):
        result = dict()
        # check the filter of selected data
        for i in range(len(fields)):
            if fields[i] == '*':
                field = self.primary
            else:
                field = fields[i]
            # print(f"index_select {index_select}")
            # print(f"filter {filter[i]}, fields:{fields[i]}")
            if filter[i] in self._select_filter_map.keys():
                result[f"{filter[i]}_{fields[i]}"] = self._select_filter_map[filter[i]](field, index_select)

        return result

    def _select_data_2(self, index_select, fields, filter, groupby=None):
        col_set = list(set(self.data[groupby]))
        col_select = {}
        for v in col_set:
            col_select[v] = []
        for i in index_select:
            for v in col_set:
                if self.data[groupby][i] == v:
                    col_select[v].append(i)
        result = {
            groupby: col_set
        }
        for col in col_set:
            for i in range(len(fields)):
                if result.get(filter[i] + '_' + fields[i]) == None:
                    result[filter[i] + '_' + fields[i]] = []
                if col_select[col] == []:
                    result[filter[i] + '_' + fields[i]].append(0)
                else:
                    result[filter[i] + '_' + fields[i]].append(
                        self._select_filter_map[filter[i]](fields[i], col_select[col])[0])

        # # check the filter of selected data
        # for i in range(len(fields)):
        #     # print(f"index_select {index_select}")
        #     result[fields[i]] = self._select_filter_map[filter[i]](fields[i], index_select)
        #     i += 1

        return result

    def get_var(self):
        return self.var

    def delete(self, action):

        if action.get('conditions'):
            cols_select = []
            conditions_select = []
            for condition in action["conditions"]:
                cols_select.append(condition['field'])
                conditions_select.append(condition['cond'])

            index_list_select = []
            for i in range(len(conditions_select)):
                cond = conditions_select[i]
                col = cols_select[i]
                if cond["operation"] not in self._condition_map:
                    print('Error! Cannot Resolve Given Input')
                    return
                tmp = self._filter(cond, col)
                index_list_select.append(tmp)
        else:
            print("ERROR! Cannot Resolve Given Input!")
            return

            # set a condition check for only one constraint
        if len(index_list_select) == 1:
            # print('Index: ', index_list_select[0])
            self._delete_data(index_list_select[0])
        else:
            index_select = index_list_select[0]
            if action['condition_logic'] == 'AND':
                # get intersection
                for i in range(1, len(index_list_select)):
                    index_select = list(set(index_select).intersection(index_list_select[i]))
                index_select.sort()
            elif action['condition_logic'] == 'OR':
                # get intersection
                for i in range(1, len(index_list_select)):
                    index_select = list(set(index_select).union(index_list_select[i]))
                index_select.sort()
            # print('Index: ', index_select)
            # delete data from table according to index in descending order
            self._delete_data(index_select)
            return

    # Select By Conditions
    def select(self, action):
        if action.get('orderby'):
            if action['orderby'] not in self.var:
                print('Error! Cannot Resolve Given Column: ', action['orderby'])
                return
        if action['fields'] == '*':
            fields = self.var
            filter = None
        else:
            fields, filter = self.check_filter(action["fields"])

        # get the corresponding index
        if action.get('conditions'):
            index_list_select = []
            for condition in action["conditions"]:
                if condition['cond']["operation"] not in self._condition_map:
                    print('Error! Cannot Resolve Given Input')
                    return
                index_list_select.append(self._filter(condition['cond'], condition['field']))
        else:
            index_list_select = [[i for i in range(len(self.data[self.var[0]]))]]

        # set a condition check for only one constraint
        index_select = index_list_select[0]
        if len(index_list_select) > 1:
            if action['condition_logic'] == 'AND':
                # get intersection
                for i in range(1, len(index_list_select)):
                    index_select = list(set(index_select).intersection(index_list_select[i]))
            elif action['condition_logic'] == 'OR':
                # get intersection
                for i in range(1, len(index_list_select)):
                    index_select = list(set(index_select).union(index_list_select[i]))
            index_select.sort()

        orderby = None
        if action.get('orderby'):
            orderby = self.data[action['orderby']]

        # print('Index: ', index_select)
        if filter and not filter == ['']:
            if "groupby" in action.keys():
                result = self._select_data_2(index_select, fields, filter, action['groupby'])
                return result, None, orderby
            else:
                result = self._select_data_3(index_select, fields, filter)
                return result, None, None
        else:
            if action.get('groupby'):
                raise Exception("ERROR!!! Cannot Run 'GROUP BY' Without Constraint!")
            result = self._select_data(index_select, fields)

        type = {}
        for var in result.keys():
            type[var] = (self.type[self.var.index(var)])

        return result, type, orderby

    def _insert(self, type, col, value):
        if type == 'int':
            value = int(value)
        elif type == 'float':
            value = float(value)
        if self.primary == col and value in self.data[self.primary]:
            raise Exception("ERROR!!! Duplicate Primary Key Value Exists!")
        self.data[col].append(value)

    def insert(self, action):
        # check the type of input, one is specify the columns they want to insert, other one does not
        # {'type': 'insert', 'table': 'table1', 'data': {'col1': 1, ' col2': 2, ' col3': 3, ' col4': 4}}
        # {'type': 'insert', 'table': 'table1', 'values': ['1', ' 2', ' 3', ' 4']}
        # inlcude data means this statement specified the columns
        if not action.get('data') == None:
            if action.get(self.primary) == None:
                raise Exception("ERROR!!! No Primary Value Provided!")
            for col in self.var:
                self.data[col].append(action.get(col))
        # otherwise, not
        else:
            # check if the provided columns matches
            if len(action['values']) != len(self.var):
                print('Can not resolve input')
            else:
                for i in range(len(action['values'])):
                    self._insert(self.type[i][0].lower(), self.var[i], action['values'][i])

        # check if the table got user defiend primary key, and append it
        if self.primary == 'index__':
            self.data[self.primary].append(self.index)
            self.index += 1

    def check_filter(self, fields):
        filter = []
        result = []
        if "(" not in fields[0]:
            return fields, ['']

        for field in fields:
            if "avg" in field.lower():
                filter.append('avg')
            elif "count" in field.lower():
                filter.append('count')
            elif "max" in field.lower():
                filter.append('max')
            elif "min" in field.lower():
                filter.append('min')
            elif "sum" in field.lower():
                filter.append('sum')
            else:
                filter.append("")
            result.append(findall(r"\((.*?)\)", field)[0])

        if "" in filter:
            for ff in filter:
                if ff != "":
                    raise Exception(f"ERROR!!! Cannot select both Column and {ff}")
        return result, filter

    def update(self, action):
        if not action.get('conditions'):
            print("ERROR! Cannot Resolve Given Input!!")
            return

        cols_select = []
        conditions_select = []
        for condition in action["conditions"]:
            cols_select.append(condition['field'])
            conditions_select.append(condition['cond'])
        index_list_select = []

        for i in range(len(conditions_select)):

            cond = conditions_select[i]
            col = cols_select[i]
            if cond["operation"] not in self._condition_map:
                print('Error! Cannot Resolve Given Input')
                return
            tmp = self._filter(cond, col)
            index_list_select.append(tmp)

        index_select = index_list_select[0]
        if "condition_logic" in action.keys():
            if action['condition_logic'] == 'AND':
                # get intersection
                for i in range(1, len(index_list_select)):
                    index_select = list(set(index_select).intersection(index_list_select[i]))
                index_select.sort()
            elif action['condition_logic'] == 'OR':
                # get intersection
                for i in range(1, len(index_list_select)):
                    index_select = list(set(index_select).union(index_list_select[i]))
                index_select.sort()

        for i in range(len(index_list_select)):
            tmp = [val for val in index_select if val in index_list_select[i]]

        data = action['data']
        for i in data.keys():
            for j in tmp:
                if self.is_number(data[i]):
                    if self.primary == i and int(data[i]) in self.data[self.primary]:
                        raise Exception("ERROR!!! Duplicate Primary Key Value Exists!")
                    self.data[i][j] = int(data[i])

                else:
                    if self.primary == i and data[i] in self.data[self.primary]:
                        raise Exception("ERROR!!! Duplicate Primary Key Value Exists!")
                    self.data[i][j] = data[i]

    # create a bplustree for the given column
    def createIndex(self, action):
        # check if the columns is in this table
        if action['col'] not in self.var:
            print("ERROR! No Column Named '%s'" % (action['col']))
            return False
        # init the name and tree
        if action['col'] in self.btrees.keys():
            print('Already Exist index on %s' % (action['col']))
            return False
        self.btrees[action['col']] = {
            'name': action['name'],
            'tree': BPlusTree()
        }
        # insert index as value where value as key
        for i in range(len(self.data[action['col']])):
            self.btrees[action['col']]['tree'].insert(self.data[action['col']][i], i)

        return True

    def dropIndex(self, action):
        cols = []
        for key, value in self.btrees.items():
            if value['name'] == action['name']:
                cols.append(key)
        if not cols == []:
            for col in cols:
                del self.btrees[col]
            return True
        return False

    def checkColumn(self, input_col):
        table_col = [*self.data]
        for ic in input_col:
            if ic not in table_col:
                print(f"Table does not have such column {ic}")
                return False
            else:
                return True

    def is_number(self, s):
        # check if string is numbers
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False
