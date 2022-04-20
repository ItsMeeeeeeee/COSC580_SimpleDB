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
def _print(res):
    """
    Print the select relations
    :param res: THis is result json like
    res = {'COL1': ['No', 'YES', 'YES', 'YES', 'No', 'YES', 'YES', 'YES', 'YES'],
       'COL2': [1.0, 7.0, 6.0, 4.0, 9.0, 11.0, 15.0, 18.0, 19.0]
       }
    :return:
    """
    tb = pt.PrettyTable()
    cols = list(res.keys())
    for col in cols:
        tb.add_column(col, res[col])
    print(tb)
