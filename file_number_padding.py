import os


def rename(filename, directory):
    parts = filename.split('.')
    new_name = ''
    for part in parts[:-1]:
        new_name += '{:04d}'.format(int(part))
        new_name += '.'
    new_name += parts.pop()
    os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
    print(new_name)


def main():
    directory = 'F:\\SecPlus'
    files = next(os.walk(directory))[2]
    for filename in files:
        rename(filename, directory)


if __name__ == '__main__':
    main()
