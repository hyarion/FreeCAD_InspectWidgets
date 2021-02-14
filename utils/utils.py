from os import path


def get_mod_path():
    return path.abspath(path.join(path.dirname(path.realpath(__file__)), path.pardir))
