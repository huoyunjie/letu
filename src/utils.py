import os

def parse_file_name(file_path, type = True):
    file_name = os.path.basename(file_path)

    if type is False:
        pos_dot = file_name.rfind('.')
        if pos_dot is not -1:
            file_name = file_name[:pos_dot]

    return file_name

# file type do not include '.'
def parse_file_type(file_path):
    (file_name, file_type) = os.path.splitext(file_path)

    pos_dot = file_type.find('.')
    if pos_dot is not -1:
        file_type = file_type[pos_dot+1:]

    return file_type

def parse_dir_path(file_path):
    dir_path = os.path.dirname(file_path)

    return dir_path