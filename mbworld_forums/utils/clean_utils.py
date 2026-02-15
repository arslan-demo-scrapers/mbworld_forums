import re
from html import unescape


def clean(text):
    if isinstance(text, (int, float)):
        return text

    text = unescape(text or '')
    # text = re.sub(u'"', u"\u201C", text or '')
    # text = re.sub(u"'", u"\u2018", text)

    for c in ['\r\n', '\n\r', u'\n', u'\r', u'\t', u'\xa0']:
        text = text.replace(c, ' ')
    return re.sub(' +', ' ', text).strip()


def clean_all(seq):
    return [clean(e) for e in seq if clean(e)]


def clean_punctuation(text):
    punctuation_re = re.compile(r'[^\w-]')
    return re.sub(punctuation_re, '', text)


def join_seq(seq, sep='\n'):
    return f'{sep}'.join(clean(e) for e in seq if clean(e))


def clean_seq(seq):
    return [clean(e) for e in seq if clean(e)]


def get_first(seq, up_to=1, sep=""):
    return f"{sep}".join([clean(e) for e in seq if clean(e)][:up_to])
