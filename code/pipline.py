#!/usr/bin/env python

import os
import langid

import conf

def get_score_path(conf, scoretype):
    score_dir = conf.score_dir
    if not os.path.isdir(score_dir):
        os.makedirs(score_dir)
    return os.path.join(conf.score_dir, 'score.{}.{}-{}'.format(scoretype,
                                                                conf.src_lang,
                                                                conf.tgt_lang))


def filter_language(conf):
    score  = []
    for lang, fpath in ((conf.src_lang, conf.src_data),
                        (conf.tgt_lang, conf.tgt_data)):
        index = 0
        with open(fpath, 'r') as inf:
            for line in inf:
                if langid.classify(line)[0] == lang:
                    s = 1
                else:
                    s = 0
                if len(score) == index:
                    score.append(s)
                else:
                    score[index] = score[index] * s
                index += 1
    with open(get_score_path(conf, 'langid'), 'w') as outf:
        for s in score:
            outf.write(str(s) + '\n')


def run(conf):
    filter_language(conf)

if __name__ == '__main__':
    run(conf)
