import re
from docutils.core import publish_string

intro = '.. contents:: Sommaire\n\n'

for i in range(10, 40):
    with open('DAVIDO/DCS_51_%03d.txt' % i) as f:
        intro += ''.join(f.readlines()[2:])

intro = intro.replace(r'procès-\nverbaux', 'procès-verbaux')
intro = re.sub(r'\(\d\)\.-', '.. [#]', intro)
intro = re.sub(r'\(\d\)', '[#]_', intro)

def remove_breaks(match):
    tiret = match.group(1)
    if tiret:
        return ''
    return ' '

intro = re.sub(r'(?<!\n|\|)(?<!-\+|=\+)(-?)\n(?!\n)', remove_breaks, intro)

def replace(char):
    def inner(match):
        tout = match.group(0)
        titre = match.group(1)
        if tout != '0.- Introduction':
            titre = tout
        chars = char * len(titre)
        return '%s\n%s\n%s' % (chars, titre, chars)
    return inner

intro = intro.replace('- INTRODUCTION -', '0.- Introduction')
intro = re.sub(r'^\d+\.\d+\.\d+\.- (.+)$', replace('.'), intro, flags=re.MULTILINE)
intro = re.sub(r'^\d+\.\d+\.- (.+)$', replace('-'), intro, flags=re.MULTILINE)
intro = re.sub(r'^\d+\.- (.+)$', replace('='), intro, flags=re.MULTILINE)

with open('intro.rst', 'w') as f:
    f.write(intro)
with open('intro.html', 'w') as f:
    f.write('<style>ul.simple { padding-left: 0; } ul { padding-left: 20px; } ul li { list-style-type: none; }</style>')
    f.write(publish_string(intro, writer_name='html'))
