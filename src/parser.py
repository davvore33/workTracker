import configparser


def getdata(path, Section):
    '''
    :param path: path of your configuration, usually into your project directory
    :param Section: sectionf of the documentation that you want to read
    :return: return a list of tuples
    '''
    parser = configparser.ConfigParser()
    parser.read(path)
    for i in parser.sections():
        if i == Section:
            return parser.items(i)
    return "Error"