#!/usr/bin/env bash

source_lang=ne
target_lang=en
rootdir="./data/processed/baseline/"

fairseq-generate \
    ${rootdir}/bin/wiki_${source_lang}_${target_lang}_bpe5000/ \
    --source-lang ${source_lang} --target-lang ${target_lang} \
    --path ${rootdir}/checkpoints/${source_lang}_${target_lang}/checkpoint_best.pt \
    --beam 5 --lenpen 1.2 \
    --gen-subset test \
    --remove-bpe=sentencepiece \
    --sacrebleu
