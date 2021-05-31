#!/usr/bin/python3

# Sebastian Slanitsch, 4CN

import string


def read_all_words(filename):
    """
    read a file with given file name
    :param filename: file to read
    :return: words in a set
    """
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
    """
    find all words with edit distance 1
    :param word: word to check
    :return: all possibilitys as a set

    >>> edit1("wand")
    {'wandh', 'waund', 'wandj', 'wsand', 'wyand', 'wanxd', 'üwand', 'woand', 'wandz', 'wandw', 'waond', 'wando', 'wnad', 'owand', 'waned', 'fwand', 'qwand', 'pwand', 'wanud', 'gwand', 'wajnd', 'wanhd', 'wandy', 'watnd', 'wandq', 'awand', 'jwand', 'zwand', 'wanqd', 'wvand', 'wapnd', 'vwand', 'wcand', 'wmand', 'wäand', 'wanßd', 'wahnd', 'wanpd', 'wad', 'wanjd', 'wandk', 'wabnd', 'xwand', 'wanid', 'wande', 'wannd', 'wtand', 'wancd', 'wanrd', 'wawnd', 'wzand', 'wanld', 'wanöd', 'swand', 'wandß', 'wanod', 'wuand', 'wantd', 'wandg', 'dwand', 'waend', 'wandb', 'wandi', 'wiand', 'bwand', 'wandp', 'warnd', 'wßand', 'wüand', 'wandl', 'wankd', 'mwand', 'waand', 'wacnd', 'wanbd', 'wandc', 'waänd', 'wpand', 'wanvd', 'cwand', 'wasnd', 'wrand', 'wavnd', 'wandü', 'lwand', 'wland', 'waknd', 'wands', 'nwand', 'wxand', 'wanad', 'wanda', 'wanüd', 'wfand', 'waynd', 'wandä', 'walnd', 'wandf', 'twand', 'kwand', 'ywand', 'iwand', 'wansd', 'wband', 'awnd', 'ewand', 'wöand', 'wqand', 'äwand', 'wandd', 'ßwand', 'wagnd', 'wandv', 'wandu', 'wwand', 'wjand', 'and', 'wandö', 'wafnd', 'wandm', 'wanyd', 'hwand', 'waqnd', 'wangd', 'wnd', 'rwand', 'wandt', 'waind', 'wanzd', 'wadnd', 'öwand', 'waönd', 'wkand', 'wamnd', 'wand', 'wanwd', 'wandn', 'whand', 'weand', 'wanmd', 'waßnd', 'wandr', 'wanäd', 'wandx', 'wgand', 'uwand', 'wan', 'wanfd', 'wnand', 'waznd', 'wadn', 'waünd', 'waxnd', 'wdand'}
    """
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
    """
    takes input from edit1 and returns only words listed in dict
    :rtype: object set of possiblitys

    >>> edit1_good("wand")
    {'wand'}
    """
    return edit1(word) & dictionary


def edit2(word):
    """
    searches for words with edit distance 2
    :param word: word to check
    :return: possibilitys as a set

    >>> edit2("wand")
    {'an', 'wank', 'wagend', 'wander', 'wlan', 'rand', 'wade', 'wanden', 'warn', 'band', 'wadi', 'wandle', 'wund', 'wend', 'wandst', 'wandet', 'ward', 'wandte', 'ad', 'wand', 'wann', 'wind', 'wandre', 'land', 'sand', 'fand', 'hand', 'andy', 'wald', 'wandel', 'tand', 'gewand', 'wahn', 'waden', 'watend'}
    """
    return {
               word
               for word in edit1(word)
               for word in edit1_good(word)
           }


def correct(word):
    """
    finds the possible corrections for word
    :param word: word to correct
    :return: possible correct words

    >>> correct("wand")
    {'wand'}
    >>> correct("wnad")
    {'wand'}
    """
    return ({word} in dictionary) or edit1_good(word) or edit2(word) or {word}


dictionary = read_all_words('/usr/share/dict/ngerman')

print(correct("wnad"))
print(correct("wand"))
print(correct('ffae'))