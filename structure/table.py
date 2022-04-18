from json import load
from bplus_tree.tree import BPlusTree
import pickle
import os

# basically, no dupulicate table name allowed

class DB_Table:
    # store each columns's variable's type to object, check it before each operation 
    def __init__(self, name, var_types=None):
        self.name = name
        # the path to save the table
        self.filePath = 'save/'
        self.cols = var_types

        # load the structure from the exist file
        if (os.path.exists(name)):
            self._load()
        else: 
            # construct btrees for all numberic columns, and check the primary key
            self.__constructTrees()
            self._checkPrimary()
        
    # check if the given columns include the primary key, set the primary key, if not, then auto increment index will be used as the primary key
    def _checkPrimary(self):
        for key, value in self.cols:
            if 'primary' in value:
                self.primary = key
                return
        # the name for default index if __index__
        self.primary =  '__index__'
        # construct the btree for primary key
        self.btrees[self.primary] = BPlusTree()
    
    def __constructTrees(self):
        for key, value in self.cols:
            # only construct new tree for numberic columns
            if 'int' in value or 'float' in value:
                self.btrees[key] = BPlusTree()

    # save the btrees to file, with the given table name
    def _save(self):
        with open(os.path.join(self.filePath, self.name), 'wb') as f:
            pickle.dump(self.btrees, f)
    
    # load the btrees from file, with the given table name
    def _load(self):
        with open(os.path.join(self.filePath, self.name), 'rb') as f:
            self.btrees = pickle.load(f)


    ######################################################################################
    # check variable's type first, then add.
    def insert(self, values):
        # if there isn't any user-assigned index, then auto increment index will be used 
        if self.primary == '__index__':
            index = max(self.btrees[self.primary].keys()) + 1

    def select(self, constriant):
        print()
    
    def delete(self, constriant):
        print()
    ######################################################################################
