#!/usr/bin/env python
# coding=utf-8

"""
A simple tokenizer for MT preprocessing.
"""

from __future__ import unicode_literals
from regex import Regex
import codecs
import sys


DEFAULT_ENCODING = 'UTF-8'


class Tokenizer(object):
    """\
    A simple tokenizer class, capable of tokenizing given strings.
    """

    def __init__(self, options={}):
        """\
        Constructor (pre-compile all needed regexes).
        """
        self.lowercase = 'lowercase' in options
        self.__spaces = Regex(r'\s+')
        self.__ascii_junk = Regex(r'[\000-\037]')
        self.__special_chars = \
                Regex(r'(([^\p{IsAlnum}\s\.\,])\2*)')
        self.__to_single_quotes = Regex(r'[`‚‘’]')
        self.__to_double_quotes = Regex(r'(\'\'|[“”„])')
        self.__no_numbers = Regex(r'([^\p{N}])([,.])([^\p{N}])')
        self.__pre_numbers = Regex(r'([^\p{N}])([,.])([\p{N}])')
        self.__post_numbers = Regex(r'([\p{N}])([,.])([^\p{N}])')

    def tokenize(self, text):
        """\
        Tokenize the given text using current settings.
        """
        # spaces to single space
        text = self.__spaces.sub(' ', text)
        # remove ASCII junk
        text = self.__ascii_junk.sub('', text)
        # separate punctuation (consecutive items of same type stay together)
        text = self.__special_chars.sub(r' \1 ', text)
        # separate dots and commas everywhere except in numbers
        text = self.__no_numbers.sub(r'\1 \2 \3', text)
        text = self.__pre_numbers.sub(r'\1 \2 \3', text)
        text = self.__post_numbers.sub(r'\1 \2 \3', text)
        # normalize quotes
        text = self.__to_single_quotes.sub('\'', text)
        text = self.__to_double_quotes.sub('"', text)
        # spaces to single space
        text = self.__spaces.sub(' ', text)
        text = text.strip() + "\n"
        if self.lowercase:
            text = text.lower()
        return text


if __name__ == '__main__':
    # parse options
    opts, filenames = getopt.getopt(sys.argv[1:], 'hle:')
    options = {}
    help = False
    encoding = DEFAULT_ENCODING
    for opt, arg in opts:
        if opt == '-l':
            options['lowercase'] = True
        elif opt == '-h':
            help = True
        elif opt == '-e':
            encoding = arg
    # display help
    if filenames > 2 or help:
        display_usage()
        sys.exit(1)
    # open input and output streams
    if len(filenames) == 2:
        fh_out = codecs.open(filenames[1], 'w', encoding)
    else:
        fh_out = codecs.getwriter(encoding)(sys.stdout)
    if len(filenames) >= 1:
        fh_in = codecs.open(filenames[0], 'r', encoding)
    else:
        fh_in = codecs.getreader(encoding)(sys.stdin)
    # process the input
    tok = Tokenizer(options)
    for line in fh_in:
        line = tok.tokenize(line)
        print >> fh_out, line,
