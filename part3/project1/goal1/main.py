composers = {'Johann': 65, 'Ludwig': 56, 'Frederic': 39, 'Wolfgang': 35}


def sort_dict_by_value(d):
    return dict(sorted(d.items(), key=lambda el: el[1]))


print(sort_dict_by_value(composers))
