import random


def generateWord(meaning, form, categories):
    '''Takes an English string, desired form, and generation
    categories. Returns a generated word.
    '''
    word = ""

    for syllable in range(random.randint(2, 5)):
        word += random.choice(categories["consonants"])
        word += random.choice(categories["vowels"])

    return {'english': meaning, 'word': word, 'form': form}
