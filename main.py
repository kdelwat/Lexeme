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

''' Allows user to select word to decline and declension, then outputs the
    declined word. '''
def decline():
    word = input("Enter word (in conlang) to decline: ")

    try:
        result = Library.findConWord(word)
    except LookupError:
        print("Word not found in database")
        return 1

    dec = IOHelper.createMenu("Select declension", Library.getAvailableDeclensions())

    output = Library.declineWord(result, dec)

    outputWord(output, "onlyconlang")

''' Outputs word according to output type: english (English first),
    onlyconlang (No English column), or conlang first. '''
def outputWord(word, outputtype):
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

''' Interface for getStatistics(). '''
def statistics():
    print("Words: " + str(Library.getStatistics()))

''' Interface for searchWords(). '''
def search():
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

def main():
        commands = {"add": add,
                    "list": list,
                    "decline": decline,
                    "statistics": statistics,
                    "search": search,
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
