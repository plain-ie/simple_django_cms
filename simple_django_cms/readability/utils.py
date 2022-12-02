import string
from nltk.corpus import cmudict
from nltk import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.sonority_sequencing import SyllableTokenizer


ph_dict = dict(cmudict.entries())


def get_words(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)
    return words


def get_sentences(text):
    return sent_tokenize(text)


def get_word_syllables(word):
    syllables = []
    word = word.lower()
    if word in ph_dict:
        for x in ph_dict[word]:
            if x.strip(string.ascii_letters):
                syllables.append(x)
        return syllables
    return syllables


def get_syllables(text):
    syllables = []
    for x in text.split():
        x = x.strip(string.punctuation)
        syllables += get_word_syllables(x)
    return syllables
