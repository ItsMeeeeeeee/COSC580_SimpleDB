from prettytable import PrettyTable


# get key by value
def get_equal_keys_dict(dict, value):
    return [k for k, v in dict.items() if v == value]


def get_equal_keys_list(list, value):
    return [index for index, v in enumerate(list) if v == value]


def get_less_keys_list(list, value):
    return [index for index, v in enumerate(list) if v < float(value)]


def get_less_equal_keys_list(list, value):
    return [index for index, v in enumerate(list) if v <= float(value)]


def get_more_keys_list(list, value):
    return [index for index, v in enumerate(list) if v > float(value)]


def get_more_equal_keys_list(list, value):
    return [index for index, v in enumerate(list) if v >= float(value)]


# format print
def _print(res, type=None, limit=None):
    """
    Print the select relations
    :param res: THis is result json like
    res = {'COL1': ['No', 'YES', 'YES', 'YES', 'No', 'YES', 'YES', 'YES', 'YES'],
       'COL2': [1.0, 7.0, 6.0, 4.0, 9.0, 11.0, 15.0, 18.0, 19.0]
       }
    :return:
    """
    if type:
        for col, value in res.items():
            if type[col][0] == 'int':
                for i in range(len(value)):
                    value[i] = int(value[i])
            elif type[col][0] == 'float':
                for i in range(len(value)):
                    value[i] = float(value[i])
            res[col] = value

    tb = PrettyTable()
    cols = list(res.keys())
    for col in cols:
        if limit:
            if limit < len(res[col]):
                tb.add_column(col, res[col][0:limit])
        else:
            tb.add_column(col, res[col])
    print(tb)


def merge_dict(result, res1):
    # merge first table into empty dict
    for k, v in res1.items():
        # if result.get(k, False):
        #     continue
        result[k] = v
    return result

def merge_result_inner(result, res1, res2, first_col, second_col):
    # for the result1
    res_cols, res_values = get_col_values_from_dict(res1)
    # for the result2
    res_cols2, res_values2 = get_col_values_from_dict(res2)
    # inner join, main table is res1?
    if len(res_values[0]) < len(res_values2[0]):
        main_table = True
    else:
        main_table = False
    if main_table:
        res_inner = []
        for index, value in enumerate(res2[first_col]):
            if value in res1[second_col]:
                res_inner.append(index)
        res_select = _select_part_data(res_inner, res_cols, res2)
        result = merge_dict(result, res_select)
        result = merge_dict(result, res2)
        return result
    else:
        res_inner = []
        for index, value in enumerate(res1[first_col]):
            if value in res2[second_col]:
                res_inner.append(index)
        res_select = _select_part_data(res_inner, res_cols, res1)
        result = merge_dict(result, res_select)
        result = merge_dict(result, res2)
        return result

def _select_part_data(index_select, fields, res1):
    result = dict()
    for index in index_select:
        for field in fields:
            if not result.get(field, False):
                result[field] = []
            result[field].append(res1[field][index])
    return result


def get_col_values_from_dict(res1):
    res_cols = []
    res_values = []
    for k, v in res1.items():
        res_cols.append(k)
        res_values.append(v)
    return res_cols, res_values



