def save_data_to_file(file, data):
    outfile = open(file, 'w')
    outfile.write(data)
    outfile.close()


def load_data_from_file(file):
    loadfile = open(file, 'r')
    return loadfile.read()
