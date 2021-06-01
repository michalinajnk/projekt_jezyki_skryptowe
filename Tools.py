import os


def directory_size(path, extension='.png'):
    list_dir = []
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
        if file.endswith(extension):  # eg: '.txt'
            count += 1
    return count


def fix_file(myFile):
    with open(myFile, 'w') as file:
        for line in file:
            if not line.isspace():
                file.write(line)

