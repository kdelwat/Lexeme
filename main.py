import Library
import IOHelper
from tabulate import tabulate

''' Interface for addWord() '''
def add():
    meaning = input("Enter meaning in English: ")
    word = input("Enter word in conlang: ")
    form = input("Enter part of speech (verb/noun/other): ")

    if Library.addWord(meaning, word, form) == 0:
        print("Word added")
    else:
        print("An error occured")

''' Interface for listWords() '''
def list():
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
    word = input("Enter word (in conlang) to decline: ")

    try:
        result = Library.findConWord(word)
    except LookupError:
        print("Word not found in database")
        return 1

    print("Select declension:")
    dec = IOHelper.createMenu(Library.getAvailableDeclensions())

    output = Library.declineWord(result, dec)

    outputWord(output, "onlyconlang")

def outputWord(word, outputtype):
    english = word['english']
    conlang = word['word']

    phonetic = Library.transcribePhonemes(conlang)
    allophonetic = Library.transcribeAllophones(phonetic)

    form = word['form']

    if outputtype == "english":
        print(tabulate([[meaning, conlang, form],
                        ["", phonetic, ""],
                        ["", allophonetic, ""]],
                        headers=['English', 'Conlang', 'Extra']))
    elif outputtype == "onlyconlang":
        print(tabulate([[conlang], [phonetic], [allophonetic]],
              headers=["Conlang"]))
    else:
        print(tabulate([[conlang, meaning, form],
                        [phonetic, "",  ""],
                        [allophonetic, "", ""]],
                        headers=['Conlang', 'English', 'Extra']))


def main():
        commands = {"add": add,
                    "list": list,
                    "decline": decline,
                    "query": Library.query,
                    "search": Library.search,
                    "generate": Library.generate,
                    "quit": quit}
        commandList = ""

        for key, value in commands.items():
                commandList = commandList + value.__name__ + ", "

        commandList = commandList[:-2] + "."
        print("Available commands: " + commandList)

        Library.loadData()

        command = input("Please enter a command: ")
        while command != "quit":
                commands[command]()
                command = input("Please enter a command: ")

if __name__ == '__main__':
        main()
