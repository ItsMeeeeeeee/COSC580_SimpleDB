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
    return [index for index, v in enumerate(list) if v > float(value)]
