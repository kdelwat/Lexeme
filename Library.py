import dataset
import random
import sys
import re
from tabulate import tabulate

from IOHelper import parseDic, parseList

db = dataset.connect('sqlite:///words.db')
phonemes = {}
allophones = {}
vowels = []
consonants = []

declensions = {}


# Transcribe from orthographic representation to phonetic representation
def transcribePhonemes(word):
        
        for current, new in phonemes.items():
                word = re.sub(current, new, word)

        word = "/" + word + "/"

        return word


def transcribeAllophones(word):
        word = word[1:-1]
        
        for current, new in allophones.items():
            word = re.sub(current, new, word)

        return word

''' Returns number of words in database. '''
def getStatistics():
        return len(db['words'])
        print("Word database contains " + str(len(db['words'])) + " words.")


'''Takes a search term. Returns tuple of two lists, the first populated with matching
    English words and the second with matching conlang words. '''
def searchWords(term):
        englishresult = db['words'].find(english=term)

        conlangresult = db['words'].find(word=term)

        return (list(englishresult), list(conlangresult))

''' Takes an English string and desired form. Returns a generated word. '''
def generateWord(meaning, form):
        word = ""

        for syllable in range(random.randint(2, 5)):
            word += random.choice(consonants) + random.choice(vowels)

        return {'english': meaning, 'word': word, 'form': form}


''' Returns declension list. '''
def getAvailableDeclensions():
        return list(declensions)


''' Declines word with declension d. Returns declined word. '''
def declineWord(word, d):
        dec = declensions[d].split("->")

        word['word'] = re.sub(dec[0], dec[1], word['word'])

        return word

''' Finds the first occurrence of term in conlang column of database and
    returns as a word. '''
def findConWord(term):
        word = db['words'].find_one(word=term)

        if word is None:
            raise LookupError
        else:
            return word

''' Finds the first occurrence of term in English column of database 
    and returns as a word. '''
def findEnglishWord(term):
    word = db['words'].find_one(english=english)

    if word is None:
        raise LookupError
    else:
        return word

''' Accepts string and searches for it in conlang words list and English words
    list. If word exists in database, returns True, otherwise returns False.
    '''
def wordExists(term):
    try:
        findConWord(term)
        findEnglishWord(term)
    except LookupError:
        return False
    else:
        return True

''' Takes type of list (full or specific form) and form. Returns list of
matching words '''
def listWords(t, f):
        outList = []

        if t == "all":
                for word in db['words']:
                        outList.append([word['english'], word['word'],  word['form']])
        elif t == "form":
                if f == "noun":
                        for word in db.query('SELECT * FROM words WHERE form LIKE "noun"'):
                                outList.append([word['english'], word['word'], word['form']])
                elif f == "verb":
                        for word in db.query('SELECT * FROM words WHERE form LIKE "verb"'):
                                outList.append([word['english'], word['word'], word['form']])
                elif f == "other":
                        for word in db.query('SELECT * FROM words WHERE form LIKE "other"'):
                                outList.append([word['english'], word['word'], word['form']])
        return outList

''' Takes three strings for meaning, word in conlang, and part of speech and
adds word to database '''
def addWord(meaning, word, form):
        db['words'].insert(dict(english=meaning, word=word, form=form))
        return 0

''' Loads all language-specific information from file. '''
def loadData():
    global phonemes
    phonemes = parseDic("phonemes.txt")
    
    global allophones
    allophones = parseDic("allophones.txt")

    global vowels
    vowels = parseList("vowels.txt")

    global consonants
    consonants = parseList("consonants.txt")

    global declensions
    declensions = parseDic("declensions.txt")
