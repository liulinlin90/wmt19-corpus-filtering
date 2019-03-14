#!/usr/bin/env python

import os
import langid
from nltk.tokenize import ToktokTokenizer
import numpy as np
import string
import re

import conf

def get_score_path(conf, scoretype):
    score_dir = conf.score_dir
    if not os.path.isdir(score_dir):
        os.makedirs(score_dir)
    return os.path.join(conf.score_dir, 'score.{}.{}-{}'.format(scoretype,
                                                                conf.src_lang,
                                                                conf.tgt_lang))

def load_score(score_path):
    result = []
    with open(score_path, 'r') as inf:
        for line in inf:
            result.append(float(line))
    return result

def filter_language(conf):
    score  = []
    score_path = get_score_path(conf, 'langid')
    if os.path.isfile(score_path):
        print('use old score file:', score_path)
        return load_score(score_path)
    for lang, fpath in ((conf.src_lang, conf.src_data),
                        (conf.tgt_lang, conf.tgt_data)):
        index = 0
        with open(fpath, 'r') as inf:
            for line in inf:
                line = line.strip()
                if langid.classify(line)[0] == lang:
                    s = 1
                else:
                    l = int(len(line)/2)
                    if l > 2 and (langid.classify(line[:l])[0] == lang or langid.classify(line[l:])[0] == lang):
                        s = 0.5
                    else:
                        s = 0
                if len(score) == index:
                    score.append(s)
                else:
                    score[index] = score[index] * s
                index += 1
    with open(score_path, 'w') as outf:
        for s in score:
            outf.write(str(s) + '\n')
    return score


def filter_length(conf):
    score  = []
    score_path = get_score_path(conf, 'length')
    if os.path.isfile(score_path):
        print('use old score file:', score_path)
        return load_score(score_path)
    toktok = ToktokTokenizer()
    punct = {}
    for i in string.punctuation:
        punct[i] = 1
    for fpath in (conf.src_data, conf.tgt_data):
        index = 0
        with open(fpath, 'r') as inf:
            for line in inf:
                line = line.strip()
                line = re.sub(r'\d+', ' ', line)
                line = set(toktok.tokenize(line))
                line = list(filter(lambda x: x not in punct, line))
                l = len(line)
                if len(score) == index:
                    score.append(l)
                else:
                    src_l = score[index]
                    max_l = max(src_l, l)
                    min_l = min(src_l, l)
                    s1 = 1
                    s2 = 1
                    if max_l - min_l > 3:
                        s1 = 1 - (max_l - min_l)/max_l
                    if max_l > 50 or min_l < 5:
                        s2 = min(50.0/(max_l + 1), min_l/8.0)
                    score[index] = min(s1, s2)
                index += 1
    with open(score_path, 'w') as outf:
        for s in score:
            outf.write(str(s) + '\n')
    return score


def filter_duplicate(conf):
    score  = []
    score_path = get_score_path(conf, 'duplicate')
    if os.path.isfile(score_path):
        print('use old score file:', score_path)
        return load_score(score_path)
    toktok = ToktokTokenizer()
    for fpath in (conf.src_data, conf.tgt_data):
        index = 0
        data = {}
        with open(fpath, 'r') as inf:
            for line in inf:
                line = line.strip()
                s = 1
                if line in data:
                    data[line] += 1
                    s = (1.0/data[line])**2
                else:
                    data[line] = 1
                if len(score) == index:
                    score.append(s)
                else:
                    score[index] = score[index] * s
                index += 1
    with open(score_path, 'w') as outf:
        for s in score:
            outf.write(str(s) + '\n')
    return score

def run(conf):
    score_lang = np.array(filter_language(conf))
    score_len = np.array(filter_length(conf))
    # check after translation quality score
    score_dup = np.array(filter_duplicate(conf))
    score_path = get_score_path(conf, 'combine')
    with open(score_path, 'w') as outf:
        for s in score_lang * score_len * score_dup:
            outf.write("%.6f" % s + '\n')


if __name__ == '__main__':
    run(conf)
