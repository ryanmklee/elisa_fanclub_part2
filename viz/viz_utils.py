from viz import viz_constants


def check_chart_args(arg_array):
    if arg_array and len(arg_array) == 3:
        return arg_array[0] in viz_constants.CHART_TYPES and \
               all(arg.isdigit() for arg in arg_array[1:]) and int(arg_array[1]) >= int(arg_array[2])
    else:
        return False
