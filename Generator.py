import random


def generateWord(meaning, form, categories, settings, formrules=None):
    '''Takes an English string, desired form, generation
    categories, settings, and optional form-specific rules.
    Returns a generated word.
    '''
    word = ""
    print(categories)

    minS = settings["minS"]
    maxS = settings["maxS"]
    defaultrule = settings["rule"]
    if form in formrules:
        rule = formrules[form]
    else:
        rule = defaultrule

    print(rule)
    for syllable in range(random.randint(minS, maxS)):
        word += generateSyllable(categories, rule)

    return {'english': meaning, 'word': word, 'form': form}


def generateSyllable(categories, rule):
    '''Takes a category dictionary and a rule. Returns a
    generated syllable.
    '''
    syllable = ""
    for place in rule:
        if isinstance(place, str):
            syllable += random.choice(categories[place])
        else:
            x = random.choice(place)
            if x is not None:
                syllable += random.choice(categories[x])
    return syllable
