#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
import itertools
import pprint
import collections
import re
import io

import unicodedata

from functools import reduce

import sys


def remove_accents(my_unicode):
    return unicodedata.normalize('NFD', my_unicode).encode('ascii', 'ignore').decode('ascii').lower()

def clean_text(*l):
    return tuple(map(remove_accents, itertools.chain(*list(map(lambda s: s.split('/'), l)))))


indices = clean_text(
    "*y****** *u ****é/f***** *i* *e* *e***",
    "********é ******r/e* ***r* ********u*",
    "*t******* **********e/********t d *n *é****",
    "é******** **n* *e* *i***/i******** *n **s****",
    "*a******* ************e/g********** *u *o****",
    "*******é ******t*/****è* d *n **l* **e*",
    "**v*** *e ****s *é*****/*e **o**** é**** *****n*",
    "*r** **********S/*t *i***** *o** l é****",
    "*n **a*** *******x/*a** *n* ****é*****",
    "**s ****r* e* ******s/*******é* *e *o***",
    "***é***** *i******/*t ***ô** ****è**",
    "**n********* ********x/*a***** ****é* *u *i*",
    "*s***** *f*******é*/à l* *u* d *n *é***",
    "*n *f******** *o*/*é*é*** *a** *e ***f***",
    "*u*** *e **c** *e *c****/***è* *e *i****",
    "*******t* *a** *e* ******s/d *n *****é**** *é****",
    "******é* **** ** ****s / *’** ****s*** é*******",
    "***o** *** ** **n* / *é******* **** ***a**",
    "***** ** *é********* / ***** *e ********",
    "É**** **********, / ******* *******u*",
    "******** *********** / ** ** ***** *******",
    "********** *é***** / ** *é**** ******",
    "*****è** ** **é****** / ** ****** ** *******",
    "*****, *’é***** é***** / ***** **** ** *é*****"
)

anagrams = clean_text(
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
    'SALLE + DEFUNT + STRESS + MONTRE / AIDE + TENTE + LUNDI + QUAND',
    'MA + DES + SEUL + PRETENTION / AN + SUD + DENTS + INTERDIRE',
    'AGE + PARE + NOMS + SOLS / DUT + CAPITULE + COMPTANT',
    'AERIEN + SORTIS + POSANT / AN + PARTI + VERDATRE',
    'VALEUREUX + MILICE / PROLIFIQUE + ROQUET',
    'ENTOURLOUPERA + EXIGUS / MUN + PNEU + MENT + MIMIS',
    'AIGREFINS + SOLENNEL / ARA + DAME + DEMONTE',
    'FORMEL + PENDRE + BECQUEE / ADOS + LUIT + PARU + ROTIR',
    'NEE + QUE + PIPIN + ELFIQUE / AGE + LENT + REND + SANDALE'
)


def build_regex(indice_part, letters):
    patterns = [
        '[%s]' % ''.join(letters)
        if indice == '*' else
        indice
        for indice in indice_part
    ]
    return re.compile('^%s$' % ''.join(patterns), re.IGNORECASE)


def parse_all_words(regex):
    # open the dictionnary and return all word matching regex
    # yield from iter(['lol', 'tyrannie', 'du', 'passe'])
    # return

    with io.open("./test.txt", "r", encoding="utf8") as f:
        for line in f.readlines():
            ascii_line = remove_accents(line)
            if regex.match(ascii_line):
                yield ascii_line.strip()


def permute_solutions(words, current_counter, expected_counter):
    if not words:
        if current_counter == expected_counter:
            yield tuple()
        return
    for current_w in words[0]:

        new_counter = current_counter + collections.Counter(current_w)
        extra_not_in_anagram = new_counter - expected_counter
        if extra_not_in_anagram:
            continue
        else:
            for result in permute_solutions(words[1:], new_counter, expected_counter):
                yield (current_w,) + result


def solve(indice, anagram):
    letters = collections.Counter(anagram.replace(' ', '').replace('+', ''))
    words_list = []
    for indice_part in indice.split(' '):
        # for each word in the indice
        regexp = build_regex(indice_part, letters)
        words_list.append(set(list(parse_all_words(regexp))))
    print('possibilities : %s' % [len(words) for words in words_list])
    for solution in permute_solutions(words_list, collections.Counter(), letters):
        yield solution


def main(numToDo):
    for i, (indice, anagram) in enumerate(zip(indices, anagrams)):
        print("[%d]%s => %s" % (i, indice, anagram))
        if i not in numToDo:
            continue
        print('\n'.join(' '.join(s) for s in solve(indice, anagram)))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        numToDo = [int(i) - 1 for i in sys.argv[1:]]
    else:
        print('give numbers bitch')
        exit()
    main(numToDo)
