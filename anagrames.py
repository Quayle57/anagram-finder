#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
import itertools
import operator
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
    "Tyrannie du passé/future fin des temps",
    "nervosité torpeurr/et sobre contrecoup",
    "attention silencieuse/hurlement d un médium",
    "éclaircie dans les cieux/irradiant un vestige",
    "narration bouillonante/gargouilles au combat",
    "*ubiquité fortuite/auprès d un halo bleu",
    "Devant le puits détruits/le trouble était profond",
    "Ires sardoniques/et mission pour l éclat",
    "Un oracle studieux/dans une cathédrale",
    "Les allers et retours/endiablés de Roger",
    "Ésperance violette/et alcôve secrète",
    "**n********* valeureux/parfois piqués au vif",
    "Esprits effarouchés/à la vue d un démon",
    "Un effroyable roi/pénétra dans le gouffre",
    "Quand le pacte se scelle/après le rituel",
    "Tourments dans les refletss/d un inquiétant dédale",
    "******é* **** ** ****s/d un sinistre é*******",
    "***o** *** ** **n*/décuplant tout impact",
    "Soins et réparations/avant de repartir",
    "Éveil miraculeux/fertile quiproquo",
    "Rugueuse exploration/en un temps minimum",
    "Infernales légions/** *é**** ******",
    "Problème de fréquence/** ****** ** *******",
    "Enfin l é***** équipe/***** **** ** *é*****",
    "*é******** d ** ****/********* ** ******",
    "Terribles dévoreurs/****** ** *******",
    "********* *é*******/****** ** *******",
    "**** ** ******é/********** * ******",
    "************ ******/****** à *** *******",
    "********* * ** *******/**â** à ** *** ******",
    "* ****** **********/****** ******* ****"
)

anagrams = clean_text(
    'ANE + PUR + DYNASTIES / DEFI + FUTS + MENT + PEURS',
    'ENTROUVERTE + SIROP / BOUC + OCRE + ENTREPOTS',
    'CONTENTIEUSE + SALINITE / MUR + NUL + DEMENT + HUMIDE',
    'UNS + LILAS + ACIDE + EXERCICE / ADIEU + VINGT + TERRAINS',
    'REANOBLIRONT + ANNULATION / GAGES + TAMBOUR + CAILLOU',
    'TURQUIFIEE + BITTOU / NU + PU + SOU + HALLE + BARDE',
    'VUES + TITRE + DUDIT + PLANTE / ABORD + FILLE + PONTE + TORTUE',
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
    'NEE + QUE + PIPIN + ELFIQUE / AGE + LENT + REND + SANDALE',
    'OR + DUC + DUEL + INVENTEE / NI + BLONDE + RESPIRANT',
    'RETROVERSER + BIDULES / LAC + DONA + RELAYANT',
    'AIDES + EN + LUTTES / CAR + NATAL + SAILLANTS',
    'MYTHONNENT + EXAUCEES / SU + ME + OUI + ATTENANTES',
    'AXE + NUL + PIED + SANCTIONS / LA + CE + BRUN + CA + CORDAGE',
    'BAL + LUIT + COMMETTANT / UN + PSEUDO + ADMIRABLES'
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


def permute_solutions(words, current_counter, expected_counter, cb_up):
    if not words:
        if current_counter == expected_counter:
            yield tuple()
        cb_up()
        return
    nb_permut_sub = nb_computation(words[1:])
    for current_w in words[0]:

        new_counter = current_counter + collections.Counter(current_w)
        extra_not_in_anagram = new_counter - expected_counter
        if extra_not_in_anagram:
            cb_up(nb_permut_sub)
            continue
        else:
            for result in permute_solutions(words[1:], new_counter, expected_counter, cb_up):
                yield (current_w,) + result


def nb_computation(words):
    return reduce(operator.mul, (len(wl) for wl in words), 1)

try:
    import progressbar

    class Progresser:
        def __init__(self, total):
            self.bar = progressbar.ProgressBar(total=total)
            self.current = 0
            self.bar.start(total)

        def up(self, nb=1):
            self.current += nb
            self.bar.update(self.current)

        def __del__(self):
            self.bar.finish()

except ImportError:
    class Progresser:
        def __init__(self, total):
            self.total = total
            self.current = 0

        def print(self):
            print('%d/%d\r' % (self.current, self.total), end='', file=sys.stderr)

        def up(self, nb=1):
            self.current += nb
            self.print()


class OrderingSolver:
    """
    sort a list of data, and alow to unapply the ordering to any other data

    >>> s = OrderingSolver((3, 2, 7, 4))
    >>> s.sort()
    (2, 3, 4, 7)
    >>> ''.join(s.unsort('abcd'))
    'badc'

    """
    def __init__(self, data):
        self.data = data

    def sort(self, key=lambda i, v: v, **kwargs):

        key_list = sorted(enumerate(self.data), key=lambda t: key(*t), **kwargs)
        self.order = {i: t[0] for i, t in enumerate(key_list)}
        return tuple(map(operator.itemgetter(1), key_list))

    def unsort(self, data):
        return tuple(data[self.order[i]] for i in range(len(data)))


def solve(indice, anagram):
    letters = collections.Counter(anagram.replace(' ', '').replace('+', ''))
    words_list = []
    for indice_part in indice.split(' '):
        # for each word in the indice
        regexp = build_regex(indice_part, letters)
        words_list.append(set(list(parse_all_words(regexp))))
    total = nb_computation(words_list)
    print('possibilities : %s => %d' % ([len(words) for words in words_list], total))
    progresser = Progresser(total)

    # sort words_list to better perfs
    orderer = OrderingSolver(words_list)
    sorted_word = orderer.sort(key=lambda i, v: len(indice.split(' ')[i]), reverse=True)
    print('optimized word_list : %s' % [len(words) for words in sorted_word])
    for solution in permute_solutions(sorted_word, collections.Counter(), letters, progresser.up):
        # output solution in right order
        yield orderer.unsort(solution)


def main(numToDo=None):
    for i, (indice, anagram) in enumerate(zip(indices, anagrams)):
        if numToDo is not None and i not in numToDo:
            continue
        print("[%d]%s => %s" % (i, indice, anagram))
        print('\n'.join(' '.join(s) for s in solve(indice, anagram)))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        numToDo = [int(i) - 1 for i in sys.argv[1:]]
    else:
        numToDo = None
    main(numToDo)
