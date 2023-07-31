def set_if_not_empty(filter_dict, key, value):
    if value != '' and value is not None:
        filter_dict[key] = value
