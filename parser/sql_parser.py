
class Parser:

    def __init__(self):
        self.operations = {
            'delete' : self._delete,
            'insert' : self._insert,
            'select' : self._select
            # 'create' : self.create,
            # 'drop' : self.drop,
            # 'show' : self.show,
            # 'update' : self.update,
            # 'use' : self.use
        }

    def parse(self, statement):
        # divide the statement into two part, operation part and constraint part
        if 'where' in statement:
            statement = statement.split('where')
        else:
            statement = statement.split('WHERE')

        base_tokens = statement[0].split(' ')
        # length of statement should greater than 1, otherwise, there is a syntax error.
        if (len(base_tokens) < 2):
            print('Syntax Error Found in: ' + str(statement[0]))
            return

        # convert the string to lower case to match the key words
        base_operation = base_tokens[0].lower()
        if (base_operation not in self.operations.keys()):
            print('Syntax Error Found in: ' + str(statement[0]))
            return

        info = self.operations[base_operation](base_tokens)

        

  #####################################################################################  
    def _select(self, tokens):
        cols = []
        index = 1
        while(not tokens[index].lower() == 'from'):
            cols.append(tokens[index])
            index += 1
        index += 1
        return {
            'type' : 'select',
            'table' : tokens[index],
            'cols' : cols
        }
        

    def _delete(self, tokens):
        if (len(tokens) != 3 or not tokens[1].lower() == 'from'):
            print('Syntax Error Found in: ' + ' '.join(tokens))
            return
        return {

            'type' : 'delete',
            'table' : tokens[2]
        }

    def _insert(self, tokens):
        if (len(tokens) != 3 or not tokens[1].lower() == 'into'):
            print('Syntax Error Found in: ' + ' '.join(tokens))
            return
        return {
            'type' : 'insert',
            'table' : tokens[2]
        }
        
    # def update(self, statement):
    #     print()
        
    # def use(self, statement):
    #     print()

    # def drop(self, statement):
    #     print()

    # def show(self, statement):
    #     print()

    # def create(self, statement):
    #     print()
#####################################################################################


    def _constraint(self, statement, result):
        print()