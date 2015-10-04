import dataset
import re

from Generator import generateWord

db = dataset.connect('sqlite:///words.db')
phonemes = {}
allophones = {}
declensions = {}
categories = {}


def transcribePhonemes(word):
    '''Transcribe from orthographic representation to phonetic
    representation.
    '''
    for current, new in phonemes.items():
        word = re.sub(current, new, word)

    word = "/" + word + "/"

    return word


def transcribeAllophones(word):
    '''Transcribe from phonetic representation to full IPA
    representation.
    '''
    word = word[1:-1]

    for current, new in allophones.items():
        word = re.sub(current, new, word)

    return word


def getStatistics():
    '''Returns number of words in database.'''
    return len(db['words'])


def exportWords(filename):
    '''Takes filename and outputs csv.'''
    allWords = db['words'].all()
    dataset.freeze(allWords, format='csv', filename=filename)
    print("Exported all words to " + filename)


def searchWords(term):
    '''Takes a search term. Returns tuple of two lists, the first
    populated with matching English words and the second with
    matching conlang words.
    '''
    englishresult = db['words'].find(english=term)

    conlangresult = db['words'].find(word=term)

    return (list(englishresult), list(conlangresult))


def getAvailableDeclensions():
    '''Returns declension list.'''
    return list(declensions)


def declineWord(word, d):
    '''Declines word with declension d. Returns declined word.'''
    dec = declensions[d].split("->")

    word['word'] = re.sub(dec[0], dec[1], word['word'])

    return word


def findConWord(term):
    '''Finds the first occurrence of term in conlang column of database and
    returns as a word.
    '''
    word = db['words'].find_one(word=term)

    if word is None:
        raise LookupError
    else:
        return word


def findEnglishWord(term):
    '''Finds the first occurrence of term in English column of database
    and returns as a word.
    '''
    word = db['words'].find_one(english=term)

    if word is None:
        raise LookupError
    else:
        return word


def wordExists(term):
    '''Accepts string and searches for it in conlang words list and English words
    list. If word exists in database, returns True, otherwise returns False.
    '''
    try:
        findConWord(term)
        findEnglishWord(term)
    except LookupError:
        return False
    else:
        return True


def listWords(t, f):
    '''Takes type of list (full or specific form) and form. Returns list of
    matching words.
    '''
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
            q = 'SELECT * FROM words WHERE form LIKE "other"'
            for word in db.query(q):
                outList.append([word['english'], word['word'], word['form']])

    return outList


def addWord(meaning, word, form):
    '''Takes three strings for meaning, word in conlang, and part of speech and
    adds word to database.
    '''
    db['words'].insert(dict(english=meaning, word=word, form=form))
    return 0


def setPhonemes(l):
    global phonemes
    phonemes = l


def setAllophones(l):
    global allophones
    allophones = l


def setCategories(l):
    global categories
    categories = l


def getCategories():
    return categories


def setDeclensions(l):
    global declensions
    declensions = l
