#!/usr/bin/python3

# Sebastian Slanitsch, 4CN

import string


def read_all_words(filename):
    with open(filename) as f:
        return {word[:-1].lower() for word in f}


def split_word(word):
    """
    Split a word in all its variations
    :param word:
    :return:
    >>> split_word("abc")
    [('', 'abc'), ('a', 'bc'), ('ab', 'c'), ('abc', '')]
    """
    return [[word[:i].lower(), word[i:].lower()] for i in range(len(word) + 1)]

def edit1(word):
    variations = split_word(word.lower())
    errors = set()
    for variation in variations:
        errors.add(variation[0] + variation[1][1:])
        if len(variation[0]) > 0 and len(variation[1]) > 0:
            errors.add(variation[0][:-1] + variation[1][0] + variation[0][-1] + variation[1][1:])
        if len(variation[1]) > 0:
            errors.add(variation[0] + variation[1][1:])
        for letter in string.ascii_lowercase + 'äöüß':
            errors.add(variation[0] + letter + variation[1])
    return errors


def edit1_good(word):
    return edit1(word) & dictionary


def edit2(word):
    return {
               word
               for word in edit1(word)
               for word in edit1_good(word)
           }


def correct(word):
    return ({word} in dictionary) or edit1_good(word) or edit2(word) or {word}


dictionary = read_all_words('/usr/share/dict/ngerman')

print(correct("wand"))
print(correct('ffae'))