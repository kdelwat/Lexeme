import random
import re


def generateWord(meaning, form, categories, settings, phonotactics,
                 formrules=None):
    '''Takes an English string, desired form, generation
    categories, settings, and optional form-specific rules.
    Returns a generated word.
    '''
    word = ""

    minS = settings["minS"]
    maxS = settings["maxS"]
    defaultrule = settings["rule"]

    if formrules is not None:
        if form in formrules:
            rule = formrules[form]
        else:
            rule = defaultrule
    else:
        rule = defaultrule

    for syllable in range(random.randint(minS, maxS)):
        word += generateSyllable(categories, rule)

    word = applyPhonotactics(word, phonotactics)

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


def applyPhonotactics(word, phonotactics):
    '''Takes dictionary of phonotactics rules and a word. Returns
    word with all rules applied.'''
    for name, rule in phonotactics.items():
        print("Applying rule: " + name)
        r = rule.split("->")
        word = re.sub(r[0], r[1], word)
    return word
