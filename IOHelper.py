''' Takes path to text file structured like so:
        example:8
        anotherexample:āçj
    And returns a dictionary with the first item of each line as the key and
    the second as the value.
'''
def parseDic(filename):
    d = {}
    with open(filename, mode="r") as f:
        for line in f:
            l = line.strip()
            if l is not None:
                lsplit = l.split(":")
                d[lsplit[0]] = lsplit[1]
    return d

''' Takes path the text file structured like so:
        a
        b
        another value
    And returns a dictionary including each item.
'''
def parseList(filename):
    l = []
    with open(filename, mode="r") as f:
        for line in f:
            l.append(line.strip())
    return l

''' Takes a list of options and creates an input menu. Returns
    the item selected by the user '''

def createMenu(options):
    for index, item in enumerate(options):
        bullet = "(" + str(index + 1) + ") "
        print(bullet + item)

    response = int(input("Enter selection: "))
    while response not in range(1, len(options) + 1):
        print("Selection not in range")
        response = int(input("Enter selection: "))

    return options[response - 1]
