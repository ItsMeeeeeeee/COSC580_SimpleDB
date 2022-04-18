from parser.sql_parser import Parser
from executer.executer import SQL_Executer


def main():
    # init the parser, executer
    p = Parser()
    executer = SQL_Executer()

    while True:
        statement = input('mysql> ')
        if statement == 'exit':
            break 
        else:
            p.parse(statement)
    print('Working!')

# load tables from the local file, each file represent a table

if __name__ == '__main__':
    main()