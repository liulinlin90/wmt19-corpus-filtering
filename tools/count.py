#!/usr/bin/env python

import operator

from nltk.tokenize import ToktokTokenizer

filepath = './data/processed/test1/en-ne/out.5000000.en'
#filepath = './data/clean/data/wikipedia_en_ne_si_test_sets/wikipedia.dev.ne-en.ne'


def count_word(filepath):
    toktok = ToktokTokenizer()
    count = {}
    with open(filepath, 'r') as inf:
        for line in inf:
            line = line.strip().lower()
            for t in toktok.tokenize(line):
                if t in count:
                    count[t] += 1
                else:
                    count[t] = 1
    outfile = filepath + '.count'
    count_sort = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
    with open(outfile, 'w') as outf:
        for line in count_sort:
            outf.write(' '.join(map(str, line)) + '\n')

def count_len(filepath):
    toktok = ToktokTokenizer()
    count = {}
    with open(filepath, 'r') as inf:
        for line in inf:
            line = line.strip().lower()
            l = len(toktok.tokenize(line))
            if l in count:
                count[l] += 1
            else:
                count[l] = 1
    outfile = filepath + '.count_len'
    count_sort = sorted(count.items(), key=operator.itemgetter(0), reverse=True)
    with open(outfile, 'w') as outf:
        for line in count_sort:
            outf.write(' '.join(map(str, line)) + '\n')


if __name__ == '__main__':
    #count_word(filepath)
    count_len(filepath)
