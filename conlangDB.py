import dataset
import random
import sys
from pyfiglet import Figlet
from tabulate import tabulate


db = dataset.connect('sqlite:///tsayowords.db')


def transcribePhonemes(word):
        sub = {'ē': 'ɛː', 'ō': 'ɔː', 'ā': 'aː', 'ts': 't͜s',
               'y': 'j', 'ő': 'ø', 'e': 'ɛ', 'o': 'ɔ'}

        for current, new in sub.items():
                word = word.replace(current, new)

        word = "/" + word + "/"

        return word


def transcribeAllophones(word):
        word = word[1:-1]

        if word[0] in ["p", "b", "t"] and word[0:3] != "t͜s":
                sub = {"p": "pʷ", "b": "bʷ", "t": "tʷ"}
                word = sub[word[0]] + word[1:]

        toned = ""
        riselevel, droplevel, vowels = 0, 0, 0

        for i, l in enumerate(word):
                try:
                        if l in ["a", "ɛ", "ɔ"]:
                                vowels += 1
                                if vowels == 1 and word[i+1] == "ː":
                                        riselevel = 1
                                        toned += l + "12"
                                elif riselevel == 1 and word[i+1] == "ː":
                                        riselevel = 2
                                        toned += l + "23"
                                elif riselevel == 2 and word[i+1] == "ː":
                                        toned += l + "3"

                                elif word[i+1] != "ː":
                                        riselevel = 0
                                        droplevel = 0
                                        toned += l

                                elif vowels != 1 and riselevel == 0 and droplevel == 0 and word[i+1] == "ː":
                                        droplevel = 1
                                        toned += l + "32"
                                elif droplevel == 1 and word[i+1] == "ː":
                                        droplevel = 2
                                        toned += l + "21"
                                elif droplevel == 2 and word[i+1] == "ː":
                                        toned += l + "1"
                        elif l == "ː":
                                toned += ""
                        else:
                                toned += l
                except Exception:
                        toned += l

        sub = {'ɔ12': 'ɔ́ː',
               'ɔ23': 'ɔ᷄ː',
               'ɔ32': 'ɔ̀ː',
               'ɔ21': 'ɔ᷅ː',
               'a12': 'áː',
               'a23': 'a᷄ː',
               'a32': 'àː',
               'a21': 'a᷅ː',
               'ɛ12': 'ɛ́ː',
               'ɛ23': 'ɛ᷄ː',
               'ɛ32': 'ɛ̀ː',
               'ɛ21': 'ɛ᷅ː'}

        for current, new in sub.items():
                toned = toned.replace(current, new)

        sub = {'ɔ1': 'ɔ̌ː',
               'ɔ3': 'ɔ̂ː',
               'a1': 'ǎː',
               'a3': 'âː',
               'ɛ1': 'ɛ̌ː',
               'ɛ3': 'ɛ̂ː'}

        for current, new in sub.items():
                toned = toned.replace(current, new)

        toned = "[" + toned + "]"

        return toned


def outputWord(word, t):
        meaning = word['english']
        tsayo = word['word']
        phonetic = transcribePhonemes(tsayo)
        allophonetic = transcribeAllophones(phonetic)
        harmony = word['harmony']
        form = word['form']

        if t == "english":
                print(tabulate([[meaning, tsayo, form],
                                ["", phonetic, harmony + " harmony"],
                                ["", allophonetic, ""]],
                               headers=['English', 'Tsāyo', 'Features']))

        elif t == "onlytsayo":
                print(tabulate([[tsayo], [phonetic], [allophonetic]],
                      headers=["Tsāyo"]))

        else:
                print(tabulate([[tsayo, meaning, form],
                                [phonetic, "", harmony + " harmony"],
                                [allophonetic, "", ""]],
                               headers=['Tsāyo', 'English', 'Features']))


def query():
        print("Word database contains " + str(len(db['words'])) + " words.")


def search():
        term = input("Enter search term: ")
        print("Results:")
        print("")
        result = db['words'].find(english=term)
        if result is not None:
                for word in result:
                        outputWord(word, "english")
                        print("")

        result = db['words'].find(word=term)
        if result is not None:
                for word in result:
                        outputWord(word, "tsayo")
                        print("")


def generateWord(meaning, form):
        word = ""
        consonants = ["p", "b", "t", "ts", "d", "k", "s", "m", "h", "y"]
        frontvowels = ["a", "e", "ő", "ā", "ē"]
        backvowels = ["o", "u", "ō"]

        if form == "other":
                harmony = 3
                for syllable in range(random.randint(2, 5)):
                        word += random.choice(consonants) + random.choice(frontvowels+backvowels)

        elif form == "verb":
                harmony = random.randint(1, 2)
                if harmony == 1:
                        vowels = frontvowels
                else:
                        vowels = backvowels

                for syllable in range(random.randint(2, 5)):
                        word += random.choice(consonants) + random.choice(vowels)

        elif form == "noun":
                harmony = random.randint(1, 2)
                if harmony == 1:
                        for syllable in range(random.randint(2, 5)):
                                if random.randint(1, 5) != 1:
                                        word += random.choice(consonants) + random.choice(frontvowels)
                                else:
                                        word += random.choice(consonants) + random.choice(backvowels)
                else:
                    for syllable in range(random.randint(2, 5)):
                        if random.randint(1, 5) != 1:
                                        word += random.choice(consonants) + random.choice(backvowels)
                        else:
                                        word += random.choice(consonants) + random.choice(frontvowels)

        if harmony == 1:
                harmonious = "front"
        elif harmony == 2:
                harmonious = "back"
        else:
                harmonious = "no"

        # final ő changes to e if following another ő
        if word[-1] == "ő" and word[-3] == "ő":
                word = word[:-1] + "e"

        return {'english': meaning, 'word': word, 'harmony': harmonious, 'form': form}


def generate(meaning=None):
        form = input("Enter word type (noun/verb/other): ")
        while form not in ["noun", "verb", "other"]:
                print("Not a valid type!")
                form = input("Enter word type (noun/verb/other): ")

        if meaning is None:
                meaning = input("Enter word meaning: ")

        result = db['words'].find_one(english=meaning)

        if result is not None:
                print("Word already exists!")
                outputWord(result, "english")
                return 0

        # generate and display words until acceptance
        accepted = "n"
        while accepted != "y":

                # generate words until there are no matches in database
                word = generateWord(meaning, form)
                while db['words'].find_one(word=word['word']) is not None:
                        word = generateWord(meaning, form)

                print(outputWord(word, "english"))
                accepted = input("Accept word? (y/n): ")

        db['words'].insert(dict(english=word['english'], word=word['word'], harmony=word['harmony'], form=word['form']))

        print("Word saved in database!")


def quit():
        sys.exit(0)


def conjugate():
        tsayo = input("Enter verb (in Tsāyo) to conjugate: ")
        word = db['words'].find_one(word=tsayo)
        if word is None:
                print("Word does not exist!")
                return 0

        print("Available aspects/tense: progressive (PROG), inchoative (INCH), terminative (TERM), habitual (HAB), prospective (PRSP), delimitative (DLM), future (FUT)")

        aspects = {"PROG": ("ba", "po"),
                   "INCH": ("tse", "tso"),
                   "TERM": ("pő", "pō"),
                   "HAB": ("ka", "bo"),
                   "PRSP": ("he", "hu"),
                   "DLM": ("bő", "pu"),
                   "FUT": ("ta", "tu")}

        atense = input("Enter aspect or tense: ")
        while atense not in aspects.keys():
                print("Invalid aspect or tense. Ensure you are using the shortened code.")
                atense = input("Enter aspect or tense: ")

        if word['harmony'] == "front":
                word['word'] = word['word'] + aspects[atense][0]
        else:
                word['word'] = word['word'] + aspects[atense][1]

        print("LOL" + word['word'])

        # final ő changes to e if following another ő
        if word['word'][-1] == "ő" and word['word'][-3] == "ő":
                word['word'] = word['word'][:-1] + "e"

        outputWord(word, "onlytsayo")


def list():
        t = input('Enter list type (all/form): ')
        outList = []

        if t == "all":
                for word in db['words']:
                        outList.append([word['english'], word['word'], word['harmony'], word['form']])
        elif t == "form":
                f = input("Enter desired form (verb/noun/other): ")
                if f == "noun":
                        for word in db.query('SELECT * FROM words WHERE form LIKE "noun"'):
                                outList.append([word['english'], word['word'], word['harmony'], word['form']])
                elif f == "verb":
                        for word in db.query('SELECT * FROM words WHERE form LIKE "verb"'):
                                outList.append([word['english'], word['word'], word['harmony'], word['form']])
                elif f == "other":
                        for word in db.query('SELECT * FROM words WHERE form LIKE "other"'):
                                outList.append([word['english'], word['word'], word['harmony'], word['form']])

        print(tabulate(outList, headers=["English", "Tsāyo", "Harmony", "Form"]))


def add():
        meaning = input("Enter meaning in English: ")
        tsayo = input("Enter word in Tsāyo: ")
        harmony = input("Enter harmony (front/back/no): ")
        form = input("Enter part of speech (verb/noun/other): ")

        db['words'].insert(dict(english=meaning, word=tsayo, harmony=harmony, form=form))
        print("Word saved in database!")


def main():
        f = Figlet(font="ogre")
        print(f.renderText("TsayoDB"))
        print("Welcome to tsayoDB! Dickhead")
        commands = {"add": add,
                    "list": list,
                    "conjugate": conjugate,
                    "query": query,
                    "search": search,
                    "generate": generate,
                    "quit": quit}
        commandList = ""

        for key, value in commands.items():
                commandList = commandList + value.__name__ + ", "

        commandList = commandList[:-2] + "."
        print("Available commands: " + commandList)

        command = input("Please enter a command: ")
        while command != "quit":
                commands[command]()
                command = input("Please enter a command: ")

if __name__ == '__main__':
        main()
