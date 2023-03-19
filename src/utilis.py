def find_values(key, json_obj, result_dict=None):
    if result_dict is None:
        result_dict = {}
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            if k == key:
                if k not in result_dict:
                    result_dict[k] = []
                result_dict[k].append(v)
            else:
                find_values(key, v, result_dict)
    elif isinstance(json_obj, list):
        for item in json_obj:
            find_values(key, item, result_dict)
    return result_dict
