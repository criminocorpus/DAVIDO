import re
from docutils.core import publish_string


def remove_breaks(match):
    tiret = match.group(1)
    if tiret:
        return ''
    return ' '


def replace(char):
    def inner(match):
        tout = match.group(0)
        titre = match.group(1)
        if tout != '0.- Introduction':
            titre = tout
        chars = char * len(titre)
        return '%s\n%s\n%s' % (chars, titre, chars)
    return inner


def to_rst(start, end):
    out = '.. contents:: Sommaire\n\n'
    for i in range(start, end+1):
        with open('DAVIDO/DCS_51_%03d.txt' % i) as f:
            out += ''.join(f.readlines()[2:])
    out = out.replace(r'procès-\nverbaux', 'procès-verbaux')
    out = re.sub(r'\(\d\)\.-', '.. [#]', out)
    out = re.sub(r'\(\d\)', '[#]_', out)
    out = re.sub(r'(?<!\n|\|)(?<!-\+|=\+)(-?)\n(?!\n)(?!- )', remove_breaks, out)
    out = out.replace('- INTRODUCTION -', '0.- Introduction')
    out = re.sub(r'^\d+\.\d+\.\d+\.- (.+)$', replace('.'), out, flags=re.MULTILINE)
    out = re.sub(r'^\d+\.\d+\.- (.+)$', replace('-'), out, flags=re.MULTILINE)
    out = re.sub(r'^\d+\.- (.+)$', replace('='), out, flags=re.MULTILINE)
    return out


def rst_to_html(rst):
    return publish_string(rst, writer_name='html')

intro = to_rst(10, 39)

with open('intro.rst', 'w') as f:
    f.write(intro)
with open('intro.html', 'w') as f:
    f.write('<style>ul.simple { padding-left: 0; } ul { padding-left: 20px; } ul li { list-style-type: none; }</style>')
    f.write(rst_to_html(intro))

liste_comptes = to_rst(208, 209)

with open('liste_comptes.rst', 'w') as f:
    f.write(liste_comptes)
with open('liste_comptes.html', 'w') as f:
    f.write(rst_to_html(liste_comptes))
