#!/usr/bin/env python

import operator

from nltk.tokenize import ToktokTokenizer

filepath = './data/processed/test1/en-ne/out.5000000.en'


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
                    count[t] = 0
    outfile = filepath + '.count'
    court_sort = sorted(count.items(), key=operator.itemgetter(0), reverse=True)
    with open(outfile, 'w') as outf:
        for line in count_sort:
            outf.write(' '.join(map(str, line)) + '\n')

if __name__ == '__main__':
    run(filepath)
