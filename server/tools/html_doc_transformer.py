from bs4 import BeautifulSoup
from sys import argv
from string import capwords

TYPORA_CSS_PATH = '/static/css/typora.css'

assert(argv[1] != 'base.html' and argv[1] != 'index.html')

with open(argv[1], 'r+', encoding='utf8') as f:
    f.seek(0)

    soup = BeautifulSoup(f, "html5lib")
    try:
        soup.head.select('style')[0].decompose()
    except IndexError:
        exit(1)  # already processed
    style = soup.new_tag('link', rel='stylesheet', href=TYPORA_CSS_PATH)
    soup.html.head.append(style)

    soup.html.title.string = soup.find_all('h2')[0].find_all('span')[0].string
    f.seek(0)
    f.write(str(soup))
    f.truncate(f.tell())
