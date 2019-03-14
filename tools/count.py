#!/usr/bin/env python

import operator

from nltk.tokenize import ToktokTokenizer

filepath = './data/clean/data/wikipedia_en_ne_si_test_sets/wikipedia.dev.ne-en.ne'


def run(filepath):
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

if __name__ == '__main__':
    run(filepath)
