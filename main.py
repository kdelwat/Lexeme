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
    t = IOHelper.chooseOption("Enter list type", ["all", "form"])

    if t == "form":
        pos = ["verb", "noun", "other"]

        f = IOHelper.chooseOption("Enter desired part of speech", pos)
    else:
        f = None

    l = Library.listWords(t, f)

    print(tabulate(l, headers=["English", "Conlang", "Form"]))


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

    outputWord(output, "onlyconlang")


def outputWordOld(word, outputtype):
    '''Outputs word according to output type: english (English first),
    onlyconlang (No English column), or conlang first.
    '''
    english = word['english']
    conlang = word['word']

    phonetic = Library.transcribePhonemes(conlang)
    allophonetic = Library.transcribeAllophones(phonetic)

    form = word['form']

    if outputtype == "english":
        print(tabulate([[english, conlang, form],
                        ["", phonetic, ""],
                        ["", allophonetic, ""]],
              headers=['English', 'Conlang', 'Extra']))

    elif outputtype == "onlyconlang":
        print(tabulate([[conlang], [phonetic], [allophonetic]],
              headers=["Conlang"]))

    else:
        print(tabulate([[conlang, english, form],
                        [phonetic, "",  ""],
                        [allophonetic, "", ""]],
              headers=['Conlang', 'English', 'Extra']))


def outputWord(word):
    table = [[], [], []]
    headers = []

    for item in word:
        if item == "word":
            table[0].append(word[item])

            phonetic = Library.transcribePhonemes(word[item])
            allophonetic = Library.transcribeAllophones(phonetic)
            table[1].append(phonetic)
            table[2].append(allophonetic)

            headers.append(item.capitalize())
        elif item == "id":
            pass
        else:
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
            outputWord(word, "onlyconlang")
            print("")


def quickgenerate():
    print("Generating using Quickgen...")


def generate():
    '''Outputs word according to output type: english (English first),
    onlyconlang (No English column), or conlang first.
    '''
    form = IOHelper.chooseOption("Enter word type", ["noun", "verb", "other"])

    english = input("Enter word in English: ")

    if Library.wordExists(english):
        print("Word already exists!")
        w = Library.findEnglishWord(english)
        outputWord(w, "english")
        return 1

    categories = Library.getCategories()

    accepted = False
    while accepted is not True:
        word = Library.generateWord(english, form, categories, wordgensettings,
                                    formrules)
        while Library.wordExists(word['word']):
            word = Library.generateWord(english, form, categories,
                                        wordgensettings, formrules)
        outputWord(word, "english")
        accepted = IOHelper.yesNo("Accept word")

    Library.addWord(word['english'], word['word'], word['form'])
    print("Wod saved in database!")


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
