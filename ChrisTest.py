from executorSQL.executorSQL import SQLExecuter
from parserSQL.parserSQL import SQLParser
import util

p = SQLParser()
action = p.parse("DELETE FROM TABLE1 WHERE COL1 >= 3 AND COL2 > 5")

data = {
    "COL1": [12, 2, 13, 7, 5, 6, 4, 18, 19],
    "COL2": [1, 7, 6, 4, 9, 11, 15, 18, 19],
    "__index__": [1, 2, 3, 4, 5, 6, 7, 8, 9]
}


def test_delete(action):
    print(action)

    def delete_data(index_delete):
        for index in index_delete:
            for col in var:
                del data[col][index]
            del data["__index__"][index]

    var = ["COL1", "COL2"]
    data = {
        "COL1": [12, 2, 13, 7, 5, 6, 4, 18, 19],
        "COL2": [1, 7, 6, 4, 9, 11, 15, 18, 19],
        "__index__": [1, 2, 3, 4, 5, 6, 7, 8, 9]
    }
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
            index_list_delete.append(util.get_equal_keys_list(data[col], cond["value"]))
        elif cond["operation"] == '<':
            index_list_delete.append(util.get_less_keys_list(data[col], cond["value"]))
        elif cond["operation"] == '>':
            index_list_delete.append(util.get_more_keys_list(data[col], cond["value"]))
        elif cond["operation"] == '<=':
            index_list_delete.append(util.get_less_equal_keys_list(data[col], cond["value"]))
        elif cond["operation"] == '>=':
            index_list_delete.append(util.get_more_equal_keys_list(data[col], cond["value"]))

    print(index_list_delete)

    # get intersection
    index_delete = index_list_delete[0]
    for i in range(1, len(index_list_delete)):
        index_delete = list(set(index_delete).intersection(index_list_delete[i]))
    index_delete.sort(reverse=True)
    print(index_delete)
    # delete data from table according to index in descending order
    delete_data(index_delete)

    print(data)


test_delete(action)
