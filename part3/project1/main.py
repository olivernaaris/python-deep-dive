def match_keys(data, valid, path):
    # path is just a string containing the current path
    # that we can use to append the extra/missing keys
    # and create a full path for the mismatched keys
    data_keys = data.keys()
    valid_keys = valid.keys()
    # we could just use data_keys ^ valid_keys
    # to get mismatched keys, but I prefer to differentiate
    # between missing and extra keys separately
    extra_keys = data_keys - valid_keys
    missing_keys = valid_keys - data_keys
    # Finally, build up the error state and message
    if missing_keys or extra_keys:
        is_ok = False
        missing_msg = ('missing keys:' +
                       ','.join({path + '.' + str(key)
                                 for key in missing_keys})
                      ) if missing_keys else ''
        extras_msg = ('extra keys:' +
                     ','.join({path + '.' + str(key)
                               for key in extra_keys})
                     ) if extra_keys else ''
        return False, ' '.join((missing_msg, extras_msg))
    else:
        return True, None


def match_types(data, template, path):
    # assume here that the keys have already been matched OK
    # but do not assume that the keys are necessarily in the same
    # order in both the data and the template
    for key, value in template.items():
        if isinstance(value, dict):
            template_type = dict
        else:
            template_type = value
        data_value = data.get(key, object())
        if not isinstance(data_value, template_type):
            err_msg = ('incorrect type: ' + path + '.' + key +
                       ' -> expected ' + template_type.__name__ +
                       ', found ' + type(data_value).__name__)
            return False, err_msg
    return True, None


t = {'a': int, 'b': int, 'c': int, 'd': int}
d = {'a': 'wrong type', 'b': 100, 'c': 200, 'd': {'wrong': 'type'}}
is_ok, err_msg = match_keys(d, t, 'some.path')
print(is_ok, err_msg)

t = {'a': int, 'b': str, 'c': {'d': int}}
d = {'a': 100, 'b': 'test', 'c': {'some': 'dict'}}
print(match_types(d, t, 'some.path'))