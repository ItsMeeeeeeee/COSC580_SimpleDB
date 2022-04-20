from executorSQL.executorSQL import SQLExecuter
from parserSQL.parserSQL import SQLParser
import util.util as util

dd = {
    "index":[0,1,2,3,4],
    "name":["Ben","TOM","Jerry","Peter","Ken"],
    "id":[0,1,2,3,4],
    "money":[4,10,10000,11111,99999999],
    "age":[15,20,25,26,40]
}


def update(action):
    """

    :param actions:
    :return:
    """
    data = action['data']
    conditions = action['conditions']

    if not checkColumn([*data]):
        return

    col_update = []
    con_update = []
    for k, v in conditions.items():
        col_update.append(k)
        con_update.append(v)

    list_update = []
    for i in range(len(con_update)):
        conu = con_update[i]
        col = col_update[i]
        if is_number(conu["value"]):
            conu["value"] = int(conu["value"])
        if conu["operation"] == '=':
            list_update.append(util.get_equal_keys_list(dd[col], conu["value"]))
        elif conu["operation"] == '<':
            list_update.append(util.get_less_keys_list(dd[col], conu["value"]))
        elif conu["operation"] == '>':
            list_update.append(util.get_more_keys_list(dd[col], conu["value"]))
        elif conu["operation"] == '<=':
            list_update.append(util.get_less_equal_keys_list(dd[col], conu["value"]))
        elif conu["operation"] == '>=':
            list_update.append(util.get_more_equal_keys_list(dd[col], conu["value"]))

    # print(list_update)
    tmp = list_update[0]
    for i in range(len(list_update)):
        tmp = [val for val in tmp if val in list_update[i]]
    for i in data.keys():
        for j in tmp:
            dd[i][j] = data[i]








def checkColumn(input_col):
    table_col = [*dd]
    for ic in input_col:
        if ic not in table_col:
            print(f"Table does not have such column {ic}")
            return False
        else:
            return True


def is_number(s):
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




if __name__ == '__main__':
    d = SQLParser().parse("update dd set money = 1, age = 3 where id > 0 AND age > 24")
    print(f'tokens : {d}')
    update(d)
    print(dd)
