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

''' Takes a list of options and a prompt. Creates an input menu. Returns
    the item selected by the user. '''
def createMenu(prompt, options):
    print(prompt + ":")
    for index, item in enumerate(options):
        bullet = "(" + str(index + 1) + ") "
        print(bullet + item)

    response = int(input("Enter selection: "))
    while response not in range(1, len(options) + 1):
        print("Selection not in range")
        response = int(input("Enter selection: "))

    return options[response - 1]

def chooseOption(prompt, options):
    olist = " ("
    for o in options[:-1]:
        olist = olist + o + "/"
    olist = olist + options[-1] + "): "

    response = input(prompt + olist)

    while response not in options:
        print("Response not in options")
        response = input(prompt + olist)

    return response

def yesNo(prompt):
    response = input(prompt + "? (y/n): ")
    while response not in ["y", "n"]:
        response = input(prompt + "? (y/n): ")

    if response == "y":
        return True
    else:
        return False
