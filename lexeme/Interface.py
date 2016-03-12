import lexeme.Library as Library
import csv
import lexeme.IOHelper as IOHelper
import sys
import os
from tabulate import tabulate

wordgensettings = {}
formrules = {}
phonotactics = {}
formatString = ""


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


def modify():
    '''Modify an existing word.'''
    try:
        conword = input("Enter word in conlang: ")
        if Library.wordExists(conlang=conword):
            word = Library.findConWord(conword, pop=False)
            outputWord(word)
        else:
            print("Word does not exist")
            return

        keys = list(word.keys())
        keys.remove("id")
        keys.append("NEW")
        keys.append("DELETE")

        another = True

        while another:
            key = IOHelper.chooseOption("Enter field to modify", keys)

            if key == "NEW":
                word = addCustomFields(word, prompt=False)
            elif key == "DELETE":
                keys.remove("NEW")
                keys.remove("DELETE")
                keys.remove("english")
                keys.remove("word")
                key = IOHelper.chooseOption("Enter field to delete", keys)
                keys.remove(key)
                del word[key]

                keys.insert(0, "english")
                keys.insert(0, "word")
                keys.append("NEW")
                keys.append("DELETE")
            else:
                if key in ["word", "english"]:
                    word[key] = input("Enter new value: ")
                else:
                    values = Library.getFieldOptions(key)
                    values.append("other")

                    v = IOHelper.chooseOption("Enter word value",
                                              values)

                    if v == "other":
                        v = input("Enter new value: ")

                    word[key] = v

            another = not IOHelper.yesNo("Finished modifying")

        # Delete word if finished modifying and add new word
        Library.findConWord(conword, pop=True)
        Library.addWord(word)

    except KeyboardInterrupt:
        pass


def listwords():
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

    if len(l) > 0:
        outputWordList(l)
    else:
        print("No words to display")


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

    print("")
    print(tabulate(table, headers=headers))
    print("")


def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")
    lexeme = """
 _
| |    _____  _____ _ __ ___   ___
| |   / _ \ \/ / _ | '_ ` _ \ / _ |
| |__|  __/>  |  __| | | | | |  __/
|_____\___/_/\_\___|_| |_| |_|\___|
                                                """
    print(lexeme)


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

    print("")
    print(tabulate(table, headers=headers))
    print("")


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


def batchgenerate():
    '''Run each word in file through generate.'''
    filename = input("Enter location of words file: ")
    try:
        with open(filename, "r") as f:
            for word in f:
                clearScreen()
                print("Generating word " + word.strip() + "...")
                generate(word.strip())
                input("Press enter to continue...")
    except FileNotFoundError:
        print("File not found! Double-check the path you are using.")
        return 1

    print("Finished batch generation!")


def importWords():
    '''Add words from csv file to database.'''
    filename = input("Enter location of word csv file: ")
    try:
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for word in reader:
                Library.addWord(word)
            print("Words successfully imported!")

    except FileNotFoundError:
        print("File not found! Double-check the path you are using.")


def generate(english=None):
    '''Interface to generateWord().'''
    if english is None:
        english = input("Enter word in English: ")

    if Library.wordExists(english=english):
        print("Word already exists!")
        w = Library.findEnglishWord(english)
        outputWord(w)
        return 1

    forms = Library.getFieldOptions("form")
    forms.append("other")

    form = IOHelper.chooseOption("Enter word form",
                                 forms)

    if form == "other":
        form = input("Enter new word form: ")

    finalised = False
    while finalised is not True:
        word = Library.generateWord(english, form, wordgensettings)
        while Library.wordExists(conlang=word['word']):
            word = Library.generateWord(english, form, wordgensettings)
        #clearScreen()
        outputWord(word, "conlang")

        accepted = IOHelper.chooseOption("Accept word", ["y", "n", "e"])
        if accepted == "y":
            finalised = True
        elif accepted == "e":
            word['word'] = input("Enter modified word: ")
            finalised = True

    word = addCustomFields(word)

    Library.addWord(word)
    print("Word saved in database!")


def addCustomFields(word, prompt=True):
    '''Take word and allow user to set custom fields. Return
    completed word.
    '''

    if prompt:
        another = IOHelper.yesNo("Add custom field")
    else:
        another = True

    while another:
        options = Library.getFields()
        options.append("other")
        field = IOHelper.chooseOption("Enter desired field to add", options)
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

        another = IOHelper.yesNo("Add custom field")

    return word


def loadData(filename=None):
    '''Loads data from config file and passes it to Library.'''
    try:
        result = IOHelper.parseConfig(filename)
    except KeyError:
        print("Config file is malformed or does not exist")
        quit()

    phonemes = result[0]
    allophones = result[1]
    declensions = result[2]
    exportformat = result[4]

    global wordgensettings
    wordgensettings = result[3]

    global formatString
    formatString = exportformat

    Library.setPhonemes(phonemes)
    Library.setAllophones(allophones)
    Library.setDeclensions(declensions)

    return 0


def exportText():
    '''Interface for exportText().'''
    filename = input("Enter filename to export: ")
    Library.exportText(filename, formatString)


def export():
    '''Interface for exportWords().'''
    filename = input("Enter filename to export: ")
    Library.exportWords(filename)
