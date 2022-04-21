from util import util
from bplus_tree import BPlusTree

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
            '=' : self._equal,
            '>' : self._bigger,
            '<' : self._smaller,
            '>=' : self._biggerAndEqual,
            '<=' : self._smallerAndEqual,
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
            return  float(value)
        return value
    def _equal(self, cond, col):
        return util.get_equal_keys_list(self.data[col], self._format(col, cond["value"]))
    def _bigger(self, cond, col):
        return util.get_more_keys_list(self.data[col], self._format(col, cond["value"]))
    def _smaller(self, cond, col):
        return util.get_less_keys_list(self.data[col], self._format(col, cond["value"]))
    def _biggerAndEqual(self, cond, col):
        return util.get_more_equal_keys_list(self.data[col], self._format(col, cond["value"]))
    def _smallerAndEqual(self, cond, col):
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
        for key, type in zip(self.var, self.type):
            if 'primary' in type:
                return key
        return 'index__'

    def _delete_data(self, index_delete):
        # sort the index list in decending order so we can remove all in once without error
        index_delete.sort(reverse=True)
        for index in index_delete:
            for col in self.var:
                del self.data[col][index]
            if self.primary == 'index__':
                del self.data[self.primary][index]
    
    # a helper function used to help select function to get corresponding info
    def _select_data(self, index_select, fields):
        result = dict()
        for index in index_select:
            for field in fields:
                if not result.get(field, False):
                    result[field] = []
                result[field].append(self.data[field][index])
        return result

########################################################################################################

    # def delete(self, action):
    #     # get intersection
        
    #     index_list_delete = self.condition_filter(action["conditions"])
    #     index_delete = index_list_delete[0]
    #     for i in range(1, len(index_list_delete)):
    #         index_delete = list(set(index_delete).intersection(index_list_delete[i]))
    #     index_delete.sort(reverse=True)
    #     # delete data from table according to index in descending order
    #     self._delete_data(index_delete)
    
    def delete(self, action):
        if action.get('conditions'):
            cols_select = []
            conditions_select = []
            for k, v in action["conditions"].items():
                cols_select.append(k)
                conditions_select.append(v)

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
            print('Index: ', index_list_select[0])
            result = self._delete_data(index_list_select[0])
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
            print('Index: ', index_select)
            # delete data from table according to index in descending order
            result = self._delete_data(index_select)
            return result
        
    def select(self, action):
        if action['fields'] == '*':
            fields = self.var
        else:    
            fields = action["fields"]
        if action.get('conditions'):
            cols_select = []
            conditions_select = []
            for k, v in action["conditions"].items():
                cols_select.append(k)
                conditions_select.append(v)

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
            index_list_select = [[i for i in range(len(self.data[self.var[0]]))]]

        # set a condition check for only one constraint
        if len(index_list_select) == 1:
            print('Index: ', index_list_select[0])
            result = self._select_data(index_list_select[0], fields)
            type = {}
            for var in result.keys():
                type[var] =(self.type[self.var.index(var)])
            return result, type
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
            print('Index: ', index_select)
            # delete data from table according to index in descending order
            result = self._select_data(index_select, fields)
            return result

    def insert(self, action):
        # check the type of input, one is specify the columns they want to insert, other one does not
        # {'type': 'insert', 'table': 'table1', 'data': {'col1': 1, ' col2': 2, ' col3': 3, ' col4': 4}}
        # {'type': 'insert', 'table': 'table1', 'values': ['1', ' 2', ' 3', ' 4']}
        # inlcude data means this statement specified the columns
        if not action.get('data') == None:
            for col in self.var:
                self.data[col].append(action.get(col))
        # otherwise, not
        else:
            # check if the provided columns matches
            if len(action['values']) != len(self.var):
                print('Can not resolve input')
            else:
                for i in range(len(action['values'])):
                    if self.type[i][0].lower() == 'int':
                        self.data[self.var[i]].append(int(action['values'][i]))
                    elif self.type[i][0].lower() == 'float':
                        self.data[self.var[i]].append(float(action['values'][i]))
                    # elif self.type[i][0].lower() == 'boolean':
                    #     self.data[self.var[i]].append(bool(action['values'][i]))
                    else:
                        self.data[self.var[i]].append(action['values'][i])

        # check if the table got user defiend primary key, and append it
        if self.primary == 'index__':
            self.data[self.primary].append(self.index)
            self.index += 1


    def update(self, action):
        """

        :param actions:
        :return:
        """
        data = action['data']
        conditions = action['conditions']

        if not self.checkColumn([*data]):
            return



        list_update = self.condition_filter(conditions)

        tmp = list_update[0]
        for i in range(len(list_update)):
            tmp = [val for val in tmp if val in list_update[i]]
        for i in data.keys():
            for j in tmp:
                self.data[i][j] = data[i]

    # create a bplustree for the given column
    def createIndex(self, action):
        # check if the columns is in this table
        if action['col'] not in self.var:
            print('ERROR! Cannot resolve the given input column!')
            return
        # init the name and tree
        self.btrees[action['col']] = {
            'name' : action['name'],
            'tree' : BPlusTree()
        }
        # insert index as value where value as key
        for i in range(len(self.data[action['col']])):
            self.btrees[action['col']]['tree'].insert(self.data[action['col']][i], i)



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

    def condition_filter(self, conditions):
        col_operate = []
        con_operate = []
        for k, v in conditions.items():
            col_operate.append(k)
            con_operate.append(v)

        result_list = []
        for i in range(len(con_operate)):
            conu = con_operate[i]
            col = col_operate[i]
            if self.is_number(conu["value"]):
                conu["value"] = int(conu["value"])
            if conu["operation"] == '=':
                result_list.append(util.get_equal_keys_list(self.data[col], conu["value"]))
            elif conu["operation"] == '<':
                result_list.append(util.get_less_keys_list(self.data[col], conu["value"]))
            elif conu["operation"] == '>':
                result_list.append(util.get_more_keys_list(self.data[col], conu["value"]))
            elif conu["operation"] == '<=':
                result_list.append(util.get_less_equal_keys_list(self.data[col], conu["value"]))
            elif conu["operation"] == '>=':
                result_list.append(util.get_more_equal_keys_list(self.data[col], conu["value"]))

            return result_list