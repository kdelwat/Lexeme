import configparser
import os.path
from distutils.sysconfig import get_python_lib
from shutil import copyfile

DEFAULT_CONFIG = 'default-config.txt'


def getParser(filename):
    print("Getting parser for", filename)
    parser = configparser.ConfigParser()

    if filename is None:
        if not os.path.isfile('lexeme-config.txt'):
            default_conf = get_python_lib() + '/lexeme/' + DEFAULT_CONFIG
            copyfile(default_conf, 'lexeme-config.txt')
        parser.read('lexeme-config.txt')
    else:
        parser.read(filename)

    return parser


def parseConfig(filename):
    '''Takes path to config file.
    Returns phonemes, allophones, declension rules, dictionary
    of word generation categories, word generation settings,
    phonotactics rules, and string export settings.
    '''
    parser = getParser(filename)

    rawphonemes = convertList(parser["TRANSCRIPTION"]["Phonemes"])
    phonemes = convertListToDic(rawphonemes)
    rawallophones = convertList(parser["TRANSCRIPTION"]["Allophones"])
    allophones = convertListToDic(rawallophones)

    declensions = {}
    for rule in parser["DECLENSION"]:
        declensions[rule] = parser["DECLENSION"][rule]

    phonotactics = []
    for rule in parser["DEFAULT-PHONOTACTICS"]:
        phonotactics.append(parser["DEFAULT-PHONOTACTICS"][rule])

    wordgencategories = {}
    for cat in parser["WORDGEN-CATEGORIES"]:
        wordgencategories[cat] = convertList(parser["WORDGEN-CATEGORIES"][cat])

    wordsettings = {}
    wordsettings["categories"] = wordgencategories
    wordsettings["phonotactics"] = phonotactics
    wordsettings["maxS"] = int(parser["WORDGEN-SETTINGS"]["MaxSyllable"])
    wordsettings["minS"] = int(parser["WORDGEN-SETTINGS"]["MinSyllable"])
    wordsettings["rule"] = parseSylRule(parser["WORDGEN-SETTINGS"]["Rule"])

    # Parse form-specific rules
    if "FormRules" in parser["WORDGEN-SETTINGS"]:
        rawformrules = parser["WORDGEN-SETTINGS"]["FormRules"]
        formrules = convertListToDic(convertList(rawformrules))
        for rule in formrules:
            formrules[rule] = parseSylRule(formrules[rule])
    else:
        formrules = None

    wordsettings["formrules"] = formrules

    # Parse form-specific phonotactics
    form_phono = {}

    if "FORM-PHONOTACTICS" in parser:
        for form in parser["FORM-PHONOTACTICS"]:
            form_phono[form] = convertList(parser["FORM-PHONOTACTICS"][form])

    wordsettings["form_phono"] = form_phono

    formatString = parser["EXPORT"]["Format"]

    return (phonemes, allophones, declensions, wordsettings,
            formatString)


def parseSylRule(string):
    cats = string.split("|")
    rule = []
    for item in cats:
        if item[0] is not "(":
            rule.append(item.lower())
        else:
            i = item.split(")")
            templist = [i[0][1:].lower()]
            freq = int(i[1])
            for j in range(1, freq):
                templist.append(None)
            rule.append(templist)
    return rule


def convertList(string):
    '''Takes a list in string form such as "1, 2, 3" and returns
    a proper List.
    '''
    return string.replace(" ", "").split(",")


def convertListToDic(l):
    '''Takes a list of strings such as "'1:2', 'a:b'" and returns
    a dictionary.
    '''
    d = {}
    for item in l:
        isplit = item.split(":")
        d[isplit[0]] = isplit[1]
    return d


def parseDic(filename):
    '''Takes path to text file structured like so:
            example:8
            anotherexample:āçj
       And returns a dictionary with the first item of each line as the key and
       the second as the value.
    '''
    d = {}
    with open(filename, mode="r") as f:
        for line in f:
            l = line.strip()
            if l is not None:
                lsplit = l.split(":")
                d[lsplit[0]] = lsplit[1]
    return d


def parseList(filename):
    '''Takes path the text file structured like so:
            a
            b
            another value
       And returns a dictionary including each item.
    '''
    l = []
    with open(filename, mode="r") as f:
        for line in f:
            l.append(line.strip())
    return l


def createMenu(prompt, options):
    '''Takes a list of options and a prompt. Creates an input menu. Returns
    the item selected by the user.
    '''
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
