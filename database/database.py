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
        cols_delete = []
        conditions_delete = []
        for k, v in action["conditions"].items():
            cols_delete.append(k)
            conditions_delete.append(v)

        index_list_delete = []
        for i in range(len(conditions_delete)):
            cond = conditions_delete[i]
            col = cols_delete[i]
            if cond["operation"] == '=':
                index_list_delete.append(util.get_equal_keys_list(self.data[col], cond["value"]))
            elif cond["operation"] == '<':
                index_list_delete.append(util.get_less_keys_list(self.data[col], cond["value"]))
            elif cond["operation"] == '>':
                index_list_delete.append(util.get_more_keys_list(self.data[col], cond["value"]))
            elif cond["operation"] == '<=':
                index_list_delete.append(util.get_less_equal_keys_list(self.data[col], cond["value"]))
            elif cond["operation"] == '>=':
                index_list_delete.append(util.get_more_equal_keys_list(self.data[col], cond["value"]))

        # get intersection
        index_delete = index_list_delete[0]
        for i in range(1, len(index_list_delete)):
            index_delete = list(set(index_delete).intersection(index_list_delete[i]))
        index_delete.sort(reverse=True)
        # delete data from table according to index in descending order
        self.delete_data(index_delete)

    def select(self, action):
        fields = action["fields"]

        # print(fields, "fields")
        def select_data(index_select):
            result = dict()
            for index in index_select:
                for field in fields:
                    if not result.get(field, False):
                        result[field] = []
                    result[field].append(self.data[field][index])
            return result

        cols_select = []
        conditions_select = []
        for k, v in action["conditions"].items():
            cols_select.append(k)
            conditions_select.append(v)

        index_list_select = []
        for i in range(len(conditions_select)):
            cond = conditions_select[i]
            col = cols_select[i]
            if cond["operation"] == '=':
                index_list_select.append(util.get_equal_keys_list(self.data[col], cond["value"]))
            elif cond["operation"] == '<':
                index_list_select.append(util.get_less_keys_list(self.data[col], cond["value"]))
            elif cond["operation"] == '>':
                index_list_select.append(util.get_more_keys_list(self.data[col], cond["value"]))
            elif cond["operation"] == '<=':
                index_list_select.append(util.get_less_equal_keys_list(self.data[col], cond["value"]))
            elif cond["operation"] == '>=':
                index_list_select.append(util.get_more_equal_keys_list(self.data[col], cond["value"]))

        # get intersection
        index_select = index_list_select[0]
        for i in range(1, len(index_list_select)):
            index_select = list(set(index_select).intersection(index_list_select[i]))
        index_select.sort(reverse=True)
        print(index_select)
        # delete data from table according to index in descending order
        result = select_data(index_select)
        print(result)

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
