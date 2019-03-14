# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
#!/bin/bash

SRC=ne
TGT=en

BPESIZE=5000
TRAIN_MINLEN=1  # remove sentences with <1 BPE token
TRAIN_MAXLEN=250  # remove sentences with >250 BPE tokens

ROOT='./'
SCRIPTS=$ROOT/tools/scripts
DATA=$ROOT/data/processed/test2
TMP=$DATA/wiki_${SRC}_${TGT}_bpe${BPESIZE}
DATABIN=$DATA/bin/wiki_${SRC}_${TGT}_bpe${BPESIZE}
mkdir -p $TMP $DATABIN

SRC_TOKENIZER="bash $SCRIPTS/indic_norm_tok.sh $SRC"
TGT_TOKENIZER="cat"  # learn target-side BPE over untokenized (raw) text
SPM_TRAIN=$SCRIPTS/spm_train.py
SPM_ENCODE=$SCRIPTS/spm_encode.py

TRAIN_SETS=(
    "en-ne/out.5000000"
)
VALID_SET="$ROOT/data/clean/data/wikipedia_en_ne_si_test_sets/wikipedia.dev.${SRC}-${TGT}"
TEST_SET="$ROOT/data/clean/data/wikipedia_en_ne_si_test_sets/wikipedia.devtest.${SRC}-${TGT}"

for FILE in "${TRAIN_SETS[@]}" ; do
    echo $SRC_TOKENIZER $DATA/$FILE.$SRC
done 
echo "pre-processing train data..."
for FILE in "${TRAIN_SETS[@]}" ; do
    $SRC_TOKENIZER $DATA/$FILE.$SRC
done > $TMP/train.$SRC
for FILE in "${TRAIN_SETS[@]}"; do
    $TGT_TOKENIZER $DATA/$FILE.$TGT
done > $TMP/train.$TGT

echo "pre-processing dev/test data..."
$SRC_TOKENIZER ${VALID_SET}.$SRC > $TMP/valid.$SRC
$TGT_TOKENIZER ${VALID_SET}.$TGT > $TMP/valid.$TGT
$SRC_TOKENIZER ${TEST_SET}.$SRC > $TMP/test.$SRC
$TGT_TOKENIZER ${TEST_SET}.$TGT > $TMP/test.$TGT

# learn BPE with sentencepiece
python $SPM_TRAIN \
  --input=$TMP/train.$SRC,$TMP/train.$TGT \
  --model_prefix=$DATABIN/sentencepiece.bpe \
  --vocab_size=$BPESIZE \
  --character_coverage=1.0 \
  --model_type=bpe

# encode train/valid/test
python $SPM_ENCODE \
  --model $DATABIN/sentencepiece.bpe.model \
  --output_format=piece \
  --inputs $TMP/train.$SRC $TMP/train.$TGT \
  --outputs $TMP/train.bpe.$SRC $TMP/train.bpe.$TGT \
  --min-len $TRAIN_MINLEN --max-len $TRAIN_MAXLEN
for SPLIT in "valid" "test"; do \
  python $SPM_ENCODE \
    --model $DATABIN/sentencepiece.bpe.model \
    --output_format=piece \
    --inputs $TMP/$SPLIT.$SRC $TMP/$SPLIT.$TGT \
    --outputs $TMP/$SPLIT.bpe.$SRC $TMP/$SPLIT.bpe.$TGT
done

# binarize data
fairseq-preprocess \
  --source-lang $SRC --target-lang $TGT \
  --trainpref $TMP/train.bpe --validpref $TMP/valid.bpe --testpref $TMP/test.bpe \
  --destdir $DATABIN \
  --joined-dictionary \
  --workers 4
