"""Pluralize English nouns

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (f8dy@diveintopython.org)"
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2002/04/19 07:04:39 $"
__copyright__ = "Copyright (c) 2002 Mark Pilgrim"
__license__ = "Python"

import re

def (matchPattern, applySearch, applyReplace):
    matchFunction = re.compile(matchPattern, re.IGNORECASE).search
    applyFunction = lambda word, searchPattern=applySearch, replacePattern=applyReplace: \
            re.compile(searchPattern, re.IGNORECASE).sub(replacePattern, word)
    return (matchFunction, applyFunction)

_samePlural = ('sheep', 'deer', 'fish', 'moose', 'aircraft', 'series', 'haiku')
_justAddS = ('delf', 'pelf', 'human', 'roman', 'lowlife')

_rules = (
    # words that are their own plural    
    (lambda word: word in _samePlural,
     lambda word: word),
    # words that are exceptions to later rules, just add "s"
    (lambda word: word in _justAddS,
     lambda word: word + 's')) + \
    map(lambda argv: apply(makeMatchAndApply, argv),
        (
            # words that end in "mouse" or "louse", change to "mice" or "lice"
            ('[ml]ouse$', '([ml])ouse$', r'\1ice'),
            # words that end in "child", change to "children"
            ('child$', 'child$', 'children'),
            # words that end in "booth", add "s"
            ('booth$', 'booth$', 'booths'),
            # words that end in "foot", change to "feet"
            ('foot$', 'foot$', 'feet'),
            # words that end in "ooth", change to "eeth"
            ('ooth$', 'ooth$', 'eeth'),
            # words that end in "leaf" or "loaf", change to "leaves" or "loaves"
            ('l[eo]af$', 'l([eo])af$', r'l\1aves'),
            # words that end in "sis", change to "ses"
            ('sis$', 'sis$', 'ses'),
            # words that end in "man", change "men"
            ('man$', 'man$', 'men'),
            # words that end in "ife", change "ives"
            ('ife$', 'ife$', 'ives'),
            # words that end in "eau", add "x"
            ('eau$', 'eau$', 'eaux'),
            # words that end in "lf", change to "lves"
            ('lf$', 'lf$', 'lves'),
            # words that end in "s", "x", or "z", add "es"
            ('[sxz]$', '$', 'es'),
            # words that end in hard "h", add "es"
            ('[^aeioudgkprt]h$', '$', 'es'),
            # words that end in "y", change to "ies"
            ('(qu|[^aeiou])y$', 'y$', 'ies'),
            # fallback: just add "s"
            ('$', '$', 's')
        )
    )

def plural(noun):
    for matchesRule, applyRule in _rules:
        if matchesRule(noun):
            result = applyRule(noun)
            break
    if noun == noun.upper():
        result = result.upper()
    return result

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        print plural(sys.argv[1])
