def transform_dict_to_list(result_dict):
    result_list = []
    for a, sub_dict in result_dict.items():
        for b, c_list in sub_dict.items():
            result_list.append({'a': a, 'b': b, 'c': c_list})
    return result_list
