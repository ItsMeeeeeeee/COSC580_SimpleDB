import prettytable as pt


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
def _print(res, type):
    """
    Print the select relations
    :param res: THis is result json like
    res = {'COL1': ['No', 'YES', 'YES', 'YES', 'No', 'YES', 'YES', 'YES', 'YES'],
       'COL2': [1.0, 7.0, 6.0, 4.0, 9.0, 11.0, 15.0, 18.0, 19.0]
       }
    :return:
    """
    for col, value in res.items():
        if type[col][0] == 'int':
            for i in range(len(value)):
                value[i] = int(value[i])
        elif type[col][0] == 'float':
            for i in range(len(value)):
                value[i] = float(value[i])
        res[col] = value

    tb = pt.PrettyTable()
    cols = list(res.keys())
    for col in cols:
        tb.add_column(col, res[col])
    print(tb)


def merge_dict(result, res1):
    for k, v in res1.items():
        if result.get(k, False):
            continue
        result[k] = v
    return result
