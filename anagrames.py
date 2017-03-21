# -*- coding: utf-8 -*-
import itertools
import pprint
import collections
import re
import io

import unicodedata

from functools import reduce


def remove_accents(my_unicode):
    return unicodedata.normalize('NFD', my_unicode).encode('ascii', 'ignore').decode('ascii').lower()

def split_slash(*l):
    return tuple(map(remove_accents, itertools.chain(*list(map(lambda s: s.split('/'), l)))))


indices = split_slash(
    "*y****** *u ****é/f***** *i* *e* *e***",
    "********é ******r/e* ***r* ********u*",
    "*t******* **********e/********t d’*n *é****",
    "é******** **n* *e* *i***/i******** *n **s****",
    "*a******* ************e/g********** *u *o****",
    "*******é ******t*/****è* d’*n **l* **e*",
    "**v*** *e ****s *é*****/*e **o**** é**** *****n*",
    "*r** **********S/*t *i***** *o** l’é****",
    "*n **a*** *******x/*a** *n* ****é*****",
    "**s ****r* e* ******s/*******é* *e *o***",
    "***é***** *i******/*t ***ô** ****è**",
    "**n********* ********x/*a***** ****é* *u *i*",
    "*s***** *f*******é*/à l* *u* d’*n *é***",
    "*n *f******** *o*/*é*é*** *a** *e ***f***",
    "*u*** *e **c** *e *c****/***è* *e *i****",
    "*******t* *a** *e* ******s/d’*n *****é**** *é****"
)

anagrams = split_slash(
    'ANE + PUR + DYNASTIES / DEFI + FUTS + MENT + PEURS',
    'ENTROUVERTE + SIROP / BOUC + OCRE + ENTREPOTS',
    'CONTENTIEUSE + SALINITE / MUR + NUL + DEMENT + HUMIDE',
    'UNS + LILAS + ACIDE + EXERCICE / ADIEU + VINGT + TERRAINS',
    'REANOBLIRONT + ANNULATION / GAGES + TAMBOUR + CAILLOU',
    'TURQUIFIEE + BITTOU / NU + PU + SOU + HALLE + BARDE',
    'VUES + TITRE + DUDIT + PLANTE, / ABORD + FILLE + PONTE + TORTUE',
    'DEROQUES + RAISINS / ON + CAS + MOT + SPIRITUEL + LE',
    'AN + ODIEUX + CULTURES / URNES + LANDE + DETACHA',
    'AERE + LEUR + SETS + TROLLS / DE + BORD + GENERALISE',
    'RECAPOTES + VENTILEE / SACRE + LEVEE + COTTE',
    'CONTREVENTA + CLAUSTRAUX / AVIS + PUIS + PIQUA + OFFRE',
    'AFFRETEURS + HOSPICES / DA + AN + DU + VOLE + ME + NU',
    'ON + OUBLI + EFFRAYER / DE + FUT + RAFLE + PERSONNAGE',
    'LE + QUE + DANS + LE + SPECTACLE / AERE + PLUS + LITRE',
    'SALLE + DEFUNT + STRESS + MONTRE / AIDE + TENTE + LUNDI + QUAND'
)


def build_regex(indice_part, letters):
    patterns = [
        '[%s]' % ''.join(letters)
        if indice == '*' else
        indice
        for indice in indice_part
    ]
    print(''.join(patterns))
    return re.compile(''.join(patterns), re.IGNORECASE)


def parse_all_words(regex):
    # open the dictionnary and return all word matching regex

    with io.open("./test.txt", "r", encoding="utf8") as f:
        for line in f.readlines():
            ascii_line = remove_accents(line)
            if regex.match(ascii_line):
                yield ascii_line


def solve(indice, anagram):
    letters = collections.Counter(anagram.replace(' ', '').replace('+', ''))
    words_list = []
    for indice_part in indice.split(' '):
        # for each word in the indice
        regexp = build_regex(indice_part, letters)
        words_list.append(list(parse_all_words(regexp)))
    print('possibilities : %s' % [len(words) for words in words_list])
    maxi = reduce(lambda a, b: a* b, [len(words) for words in words_list])
    for i, words in enumerate(itertools.product(*words_list)):
        print("%d/%d permutation tested\r" % (i, maxi), end='')
        # words is a tuple of valide permutations
        ctr_letters = collections.Counter()
        for word in words:
            ctr_letters.update(word)

            if (ctr_letters - letters):
                break
        if ctr_letters == letters:
            yield words


def main():

    for indice, anagram in zip(indices, anagrams):
        print("%s => %s" % (indice, anagram))
        print(list(solve(indice, anagram)))
        break

if __name__ == '__main__':
    main()