
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

    def delete(self, action):
        pass

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


