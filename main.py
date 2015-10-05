import Library
import IOHelper
import argparse
import sys

from tabulate import tabulate

wordgensettings = {}
formrules = {}


def add():
    '''Interface for addWord().'''
    meaning = input("Enter meaning in English: ")
    word = input("Enter word in conlang: ")
    form = input("Enter part of speech (verb/noun/other): ")

    if Library.addWord(meaning, word, form) == 0:
        print("Word added")
    else:
        print("An error occured")


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


def quickgenerate():
    print("Generating using Quickgen...")


def generate():
    '''Interface to generateWord().'''
    form = IOHelper.chooseOption("Enter word type", ["noun", "verb", "other"])

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

    Library.addWord(word['english'], word['word'], word['form'])
    print("Word saved in database!")


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
    parser.add_argument("-g", "--generator", choices=["quickgen", "builtin"],
                        help="select generator to use")
    args = parser.parse_args()

    commands = {"add": add,
                "list": list,
                "decline": decline,
                "statistics": statistics,
                "search": search,
                "generate": generate,
                "export": export,
                "quit": quit}

    if args.generator == "quickgen":
        commands["generate"] = quickgenerate

    commandList = ""
    for key in commands.keys():
        commandList = commandList + key + ", "

    commandList = commandList[:-2] + "."
    print("Available commands: " + commandList)

    loadData("config.txt")

    command = input("Please enter a command: ")
    while command != "quit":
        commands[command]()
        command = input("Please enter a command: ")

if __name__ == '__main__':
        main()
