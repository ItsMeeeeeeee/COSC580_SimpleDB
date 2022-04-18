from executer.executer import SQL_Executer

def main():
    # init the parser, executer
    executer = SQL_Executer()

    while True:
        statement = input('mysql> ')
        if statement == 'exit':
            break 
        else:
            executer.execute(statement)
    # print('Working!')

if __name__ == '__main__':
    main()