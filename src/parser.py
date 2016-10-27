import configparser


def getDict(path, Section = None):
    '''
    :param path: path of your configuration, usually into your project directory
    :param Section: sectionf of the documentation that you want to read
    :return: return a list of tuples
    '''
    parser = configparser.ConfigParser()
    parser.read(path)
    data = dict()
    for i in parser.sections():
        elems = parser.items(i)
        for elem in elems:
            elemDict = dict()
            elemDict[elem[0]] = elem[1]
        data[i] = elemDict
    if Section is not None:
        return data[Section]
    else:
        return data


def getList(path, Section):
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
    raise BaseException("Error")


def writedata(data, path):
    parser = configparser.ConfigParser()
    for elem in data.keys():
        dato = data[elem]
        parser[elem] = dato

    with open(path, 'w') as configfile:
        parser.write(configfile)
