import Library
import IOHelper
import argparse
import sys

from tabulate import tabulate

wordgensettings = {}
formrules = {}


def add():
    '''Interface for addWord().'''
    word = {}
    word['english'] = input("Enter meaning in English: ")
    word['word'] = input("Enter word in conlang: ")

    forms = Library.getFieldOptions("form")
    forms.append("other")

    form = IOHelper.chooseOption("Enter word form",
                                 forms)
    if form == "other":
        form = input("Enter new word form: ")

    word['form'] = form

    word = addCustomFields(word)
    Library.addWord(word)
    print("Word saved in database!")


def list():
    '''Interface for listWords().'''
    t = IOHelper.chooseOption("Enter list type", ["all", "field"])

    if t == "field":
        fields = Library.getFields()

        f = IOHelper.chooseOption("Enter desired field", fields)

        options = Library.getFieldOptions(f)

        o = IOHelper.chooseOption("Enter option to list", options)

        l = Library.listWords(t, f, o)
    else:
        l = Library.listWords(t)

    outputWordList(l)


def quit():
    sys.exit(0)


def decline():
    ''' Allows user to select word to decline and declension, then outputs the
    declined word.
    '''
    word = input("Enter word (in conlang) to decline: ")

    try:
        result = Library.findConWord(word)
    except LookupError:
        print("Word not found in database")
        return 1

    prompt = "Select declension"
    dec = IOHelper.createMenu(prompt, Library.getAvailableDeclensions())

    output = Library.declineWord(result, dec)

    outputWord(output, "conlang")


def outputWordList(wordList):
    '''Take a list of words. Output list of words in table.'''
    table = []
    headers = ["English", "Conlang"]

    for word in wordList:
        row = []
        row.append(word["english"])
        row.append(word["word"])
        for item in word:
            if item not in ["english", "word", "id"]:
                row.append(word[item])
        table.append(row)

    for item in wordList[0]:
        if item not in ["english", "word", "id"]:
            headers.append(item.capitalize())

    print(tabulate(table, headers=headers))


def outputWord(word, first="english"):
    '''Take word dictionary and optional first column. Output
    word in a table.
    '''
    table = [[], [], []]
    headers = []

    phonetic = Library.transcribePhonemes(word["word"])
    allophonetic = Library.transcribeAllophones(phonetic)

    if first == "english":
        table[0].append(word["english"])
        table[1].append("")
        table[2].append("")
        headers.append("English")

        table[0].append(word["word"])
        table[1].append(phonetic)
        table[2].append(allophonetic)
        headers.append("Conlang")
    elif first == "conlang":
        table[0].append(word["word"])
        table[1].append(phonetic)
        table[2].append(allophonetic)
        headers.append("Conlang")

        table[0].append(word["english"])
        table[1].append("")
        table[2].append("")
        headers.append("English")

    for item in word:
        if item not in ["word", "english", "id"]:
            table[0].append(word[item])
            table[1].append("")
            table[2].append("")
            headers.append(item.capitalize())

    print(tabulate(table, headers=headers))


def statistics():
    '''Interface for getStatistics().'''
    print("Words: " + str(Library.getStatistics()))


def search():
    '''Interface for searchWords().'''
    term = input("Enter search term: ")

    results = Library.searchWords(term)

    if len(results[0]) == 0 and len(results[1]) == 0:
        print("Word not found")
    else:
        for word in results[0]:
            outputWord(word, "english")
            print("")

        for word in results[1]:
            outputWord(word, "conlang")
            print("")


def generate():
    '''Interface to generateWord().'''
    forms = Library.getFieldOptions("form")
    forms.append("other")

    form = IOHelper.chooseOption("Enter word form",
                                 forms)

    if form == "other":
        form = input("Enter new word form: ")

    english = input("Enter word in English: ")

    if Library.wordExists(english):
        print("Word already exists!")
        w = Library.findEnglishWord(english)
        outputWord(w)
        return 1

    categories = Library.getCategories()

    accepted = False
    while accepted is not True:
        word = Library.generateWord(english, form, categories, wordgensettings,
                                    formrules)
        while Library.wordExists(word['word']):
            word = Library.generateWord(english, form, categories,
                                        wordgensettings, formrules)
        outputWord(word, "conlang")
        accepted = IOHelper.yesNo("Accept word")

    word = addCustomFields(word)

    Library.addWord(word)
    print("Word saved in database!")


def addCustomFields(word):
    '''Take word and allow user to set custom fields. Return
    completed word.
    '''

    while IOHelper.yesNo("Add custom field"):
        options = Library.getFields()
        options.append("other")
        field = IOHelper.chooseOption("Enter desired field", options)
        if field == "other":
            new = input("Enter new field: ")
            value = input("Enter word value: ")
            word[new] = value
        else:
            values = Library.getFieldOptions(field)
            values.append("other")

            v = IOHelper.chooseOption("Enter word value",
                                      values)

            if v == "other":
                v = input("Enter new word value: ")

            word[field] = v
    return word


def loadData(filename):
    '''Loads data from config file and passes it to Library.'''
    result = IOHelper.parseConfig(filename)
    phonemes = result[0]
    allophones = result[1]
    declensions = result[2]
    wordgencats = result[3]

    global wordgensettings
    wordgensettings = result[4]

    global formrules
    formrules = result[5]

    Library.setPhonemes(phonemes)
    Library.setAllophones(allophones)
    Library.setCategories(wordgencats)
    Library.setDeclensions(declensions)


def export():
    '''Interface for exportWords().'''
    filename = input("Enter filename to export: ")
    Library.exportWords(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", help="set database file")
    args = parser.parse_args()

    if args.database is not None:
        Library.loadDatabase(args.database)
    else:
        Library.loadDatabase()

    commands = {"add": add,
                "list": list,
                "decline": decline,
                "statistics": statistics,
                "search": search,
                "generate": generate,
                "export": export,
                "quit": quit}

    commandList = ""
    for key in commands.keys():
        commandList = commandList + key + ", "

    commandList = commandList[:-2] + "."
    print("Available commands: " + commandList)

    loadData("config.txt")

    while True:
        command = input("Please enter a command: ")
        if command in commands:
            commands[command]()
        else:
            print("Invalid command")

if __name__ == '__main__':
        main()
