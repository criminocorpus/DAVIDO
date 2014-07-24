# coding: utf-8

from __future__ import unicode_literals
from io import open	
import re
from docutils.core import publish_string


def remove_breaks(match):
    tiret = match.group(1)
    if tiret:
        return ''
    return ' '


def replace(char, big=False):
    def inner(match):
        tout = match.group(0)
        titre = match.group(1)
        if tout != '0.- Introduction':
            titre = tout
        titre = titre.rstrip('.')
        chars = char * len(titre)
        out = titre + '\n' + chars
        if big:
            out = chars + '\n' + out
        return out
    return inner


def to_rst(start, end):
    out = '.. contents:: Sommaire\n\n'
    for i in range(start, end+1):
        with open('DAVIDO/DCS_51_%03d.txt' % i) as f:
            content = ''.join(f.readlines()[2:])
            out += content

    out = out.replace('procès-\nverbaux', 'procès-verbaux')
    out = out.replace('procès-\nverbal', 'procès-verbal')
    out = re.sub(r'(?<!\n|\|)(?<!-\+|=\+)(-?)\n(?!\n)(?!- )', remove_breaks, out)

    out = re.sub(r'\(\d\)\.-', '.. [#]', out)
    out = re.sub(r'\(\d\)', '[#]_', out)

    out = out.replace('- INTRODUCTION -', '0.- Introduction')
    out = re.sub(r'^\d+\.\d+\.\d+\.\d+\.- (.+)$', replace('-'), out, flags=re.MULTILINE)
    out = re.sub(r'^\d+\.\d+\.\d+\.- (.+)$', replace('='), out, flags=re.MULTILINE)
    out = re.sub(r'^\d+\.\d+\.- (.+)$', replace('-', True), out, flags=re.MULTILINE)
    out = re.sub(r'^\d+\.- (.+)$', replace('=', True), out, flags=re.MULTILINE)
    return out


def rst_to_html(rst):
    return publish_string(rst, writer_name='html').decode('utf-8')

intro = to_rst(10, 39)

with open('intro.rst', 'w') as f:
    f.write(intro)
with open('intro.html', 'w') as f:
    f.write('<style>.contents ul.simple { padding-left: 0; } .contents ul { padding-left: 20px; } .contents ul li { list-style-type: none; }</style>')
    f.write(rst_to_html(intro))

liste_comptes = to_rst(208, 209)

with open('liste_comptes.rst', 'w') as f:
    f.write(liste_comptes)
with open('liste_comptes.html', 'w') as f:
    f.write(rst_to_html(liste_comptes))

series = to_rst(40, 144)

with open('series.rst', 'w') as f:
    f.write(series)
with open('series.html', 'w') as f:
    f.write('<style>.contents ul.simple { padding-left: 0; } .contents ul { padding-left: 20px; } .contents ul li { list-style-type: none; }</style>')
    f.write(rst_to_html(series))

