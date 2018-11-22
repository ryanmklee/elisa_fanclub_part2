def read_variables(dictionary, *variables):
    return (dictionary[name] for name in variables)


def write_variables(dictionary, **variables):
    for name, value in variables.items():
        dictionary[name] = value

