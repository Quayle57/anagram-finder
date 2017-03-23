# -*- coding: utf-8 -*-
import itertools
import io
import sys
import re
import difflib

if len(sys.argv) > 1:
    numToDo = [int(i) - 1 for i in sys.argv[1:]]
else:
    print('give numbers bitch')
    exit()

indices = [
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
    "*******t* *a** *e* ******s/d’*n *****é**** *é****",
    "******é* **** ** ****s / *’** ****s*** é*******",

]

question = [
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
    'MA + DES + SEUL + PRETENTION / AN + SUD + DENTS + INTERDIRE'
]

data = []
for i in range(len(indices) - 1):
    # Preparation des possibility
    fquestion = question[i].replace(' ', '').replace('+', '').lower().split('/')
    data.append({'question': fquestion, 'indice': indices[i], 'p1': "", 'p2': "", 'res1': [], 'res2': []})
    p = question[i].lower().split('/')
    for l in p[0]:
        if l != ' ' and l != '+' and l not in data[i]['p1']:
            data[i]['p1'] += l
    for l in p[1]:
        if l != ' ' and l != '+' and l not in data[i]['p2']:
            data[i]['p2'] += l
    data[i]['p1'] = "[" + data[i]['p1'] + "]"
    data[i]['p2'] = "[" + data[i]['p2'] + "]"

    # Preparation des indices
    ind = indices[i].split('/')
    data[i]['i1'] = ind[0].split(' ')
    data[i]['i2'] = ind[1].split(' ')

# Preparation de la liste de mots tab
tab = None
with io.open("./test.txt", "r", encoding="utf8") as f:
    t = f.read()
    tab = t.split('\n')


def generate_regex(input, poss):
    # poss = '.'
    res = ""
    nb = 0
    for i in input:
        if i == '*':
            nb += 1
        else:
            if nb is not 0:
                res += poss + '{%d}' % nb
            nb = 0
            res += i
    if nb is not 0:
        res += poss + '{%d}' % nb
    return res


def match_regex(word):
    res = []
    for elem in tab:
        if re.fullmatch(word, elem) is not None:
            res.append(elem)
    return res


def iterMatch(j, key):
    res = ''
    for i in qu['i' + key]:
        regex = generate_regex(i, qu['p' + key])
        r = match_regex(regex)
        res += '%d resultat(s) pour %s avec %s: \n' % (len(r), i, regex)
        data[j]['res' + key].append(r)
        rtab = '\n'.join(r)
        # res += rtab + '\n\n'
    return res


compTab = []


def retTab(resTab):
    return list(itertools.product(*resTab))


def calcRatio(qu, rTab):
    toRet = ''
    ratioTab = []
    for elem in rTab:
        pElem = ''.join(str(i) for i in elem)
        pureElem = ''.join(sorted(pElem))
        pureQ = ''.join(sorted(qu['question'][0]))
        ratio = difflib.SequenceMatcher(None, pureElem, pureQ).ratio()
        if ratio > 0.8:
            ratioTab.append((ratio, elem))
    ratioTab.sort(key=lambda tup: tup[0], reverse=True)
    for r in ratioTab:
        toRet += '%f %s\n' % (r[0], ' '.join(r[1]))
    return toRet


for j in numToDo:
    qu = data[j]
    res = "Question %d\n" % (j + 1)
    res += "Indices : %s\n" % qu['indice']
    res += ' '.join(qu['question']) + '\n\n'

    res += iterMatch(j, '1') + '\n'
    res += iterMatch(j, '2') + '\n'
    res += calcRatio(qu, retTab(qu['res1'])) + '\n'
    res += calcRatio(qu, retTab(qu['res2']))

    with open("question%d.txt" % (j + 1), 'w') as f:
        print(res, file=f)

    print("Question %d ecrite" % (j + 1))
