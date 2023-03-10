import numpy as np


def try_float(content_has_floats):
    """ Catches Value errors and skips "........" String in data
    :param content_has_floats: content containing floats and possible strings """

    try:
        return float(content_has_floats)
    except ValueError:
        pass


def convert(content, delimiter=None):
    """ Convert a list of strings to a numpy matrix
    :param content: list of strings
    :param delimiter: None or string """

    data = []
    for line in content:
        l_data = [try_float(f) for f in line.split(delimiter)]  # line data as floats
        # if line is int:
        # continue
        data.append(l_data)
    return np.array(data)


def convert_to_string(data_in, delimiter):
    """ Converts a numpy matrix to a string
    :param data_in: numpy matrix
    :param str delimiter: data delimiter """

    string = []
    for col in data_in:
        string.append(delimiter.join([str(f) for f in col]))
    return '\n'.join(string)


