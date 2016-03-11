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

    if form in settings["form_phono"]:
        word = applyPhonotactics(word, settings["form_phono"][form])

    return {'english': meaning, 'word': word, 'form': form}


def generateSyllable(categories, rule):
    '''Takes a category dictionary and a rule. Returns a
    generated syllable.
    '''
    syllable = ""
    for place in rule:
        # Choose whether to include optional category
        if place[0] == "[":
            if random.randint(1, 2) == 1:
                category = chooseRandomCategory(place)
                syllable += random.choice(categories[category])

        # Include mandatory list
        elif place[0] == "{":
            category = chooseRandomCategory(place)
            syllable += random.choice(categories[category])

        # Include single category
        else:
            syllable += random.choice(categories[place])

    return syllable


def chooseRandomCategory(rule):
    rule = rule[1:-1]
    categories = rule.split("/")
    return random.choice(categories)


def applyPhonotactics(word, phonotactics):
    '''Takes list of phonotactics rules and a word. Returns
    word with all rules applied.'''
    for rule in phonotactics:
        r = rule.split("->")
        word = re.sub(r[0], r[1], word)
    return word
