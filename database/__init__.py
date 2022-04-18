

from email.policy import default


class Table:
    def __init__(self, name, var_type):
        self.name = name
        self.var = []
        self.type = []
        self.data = {}
        self._init_var_type(var_type)
        for col in self.var:
            self.data[col] = []
        self.primary = self._checkPrimary()
        self.index = 0
        self.data[self.primary] = []

    def _init_var_type(self, var_type):
        for var, type in self.var_type.items():
            self.var.append(var)
            self.type.append(type)

    def _checkPrimary(self):
        for key, type in self.var_type.items():
            if 'primary key' in type:
                return key
        return '__index__'

    def delete(self):
        print(1)
        print(1)
        print(1)
        print(1)
        print(1)
        print(1)
        print(1)

        pass
    
    def insert(self, action):
        if not action.get('data', default=None) == None:
            for col in self.var:
                self.data[col].append(action.get(col, default=None))
        # else:

        # check if the table got user defiend primary key, and append it
        if self.primary == '__index__':
            index = self.index 
            self.index += 1
            self.data[self.primary].append(index)

        # append other values 
        

