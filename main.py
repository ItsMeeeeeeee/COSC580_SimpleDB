
from executorSQL import *

def main():
    e = executorSQL.SQLExecuter()
    while (True):
        statement = input("sdb> ")
        e.execute(statement)

if __name__ == '__main__':
    main()