import util


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
        return '__index__'

    def delete_data(self, index_delete):
        for index in index_delete:
            for col in self.var:
                del self.data[col][index]
            if self.primary == '__index__':
                del self.data[self.primary][index]

    def delete(self, action):

        # get intersection
        index_list_delete = self.condition_filter(action["conditions"])
        index_delete = index_list_delete[0]
        for i in range(1, len(index_list_delete)):
            index_delete = list(set(index_delete).intersection(index_list_delete[i]))
        index_delete.sort(reverse=True)
        # delete data from table according to index in descending order
        self.delete_data(index_delete)

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
                    self.data[self.var[i]].append(action['values'][i])

        # check if the table got user defiend primary key, and append it
        if self.primary == '__index__':
            index = self.index
            self.index += 1
            self.data[self.primary].append(index)

        # append other values

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