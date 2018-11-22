CONSTRUCTOR_TAG = "built-in method"
CONSTRUCTOR_ENDING = " constructor"
METHOD_TAG = "method"

def read_variables(dictionary, *variables):
    return (dictionary[name] for name in variables)


def write_variables(dictionary, **variables):
    for name, value in variables.items():
        dictionary[name] = value


def extract_constructor(function_name):
    extracted = None

    if function_name.find(CONSTRUCTOR_TAG) != -1:
        extracted = function_name.split()[-1] + CONSTRUCTOR_ENDING

    return extracted


def extract_method(function_name):
    extracted = None

    if function_name.find(METHOD_TAG) != -1:
        split = function_name.split()
        extracted = split[3].strip("'") + "." + split[1].strip("'")

    return extracted