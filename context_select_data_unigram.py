# coding:utf-8

import codecs

import os, sys
import math


def readDic(file_name, separator_words):
    f1 = codecs.open(file_name, 'r', encoding='utf8')
    dic = {}
    while 1:
        line = f1.readline()
        if len(line) == 0:
            break
        params = line.strip().replace('\r\n', '').split(separator_words)

        # params是切片
        ngrams = params
        for ngram in ngrams:
            ngram = ngram.strip()
            if ngram in dic:
                dic[ngram] = dic[ngram] + 1
            else:
                dic[ngram] = 1
    f1.close

    return dic


def sentence_score(selection_file, factor, selected_ngrams, dict_all_ngrams, separator_words):
    f2 = codecs.open(selection_file, 'r', encoding='utf8')
    while 1:
        line = f2.readline()
        if len(line) == 0:
            break
        line_clear = line.strip().replace('\r\n', '')
        params = line_clear.split(separator_words)

        # set sentence score
        score = 0
        ngrams = params

        for ngram in ngrams:
            ngram = ngram.strip()
            selected_val = 0
            if ngram in selected_ngrams:
                selected_val = selected_ngrams[ngram]
            ng_score = dict_all_ngrams[ngram] * math.exp(-1 * factor * selected_val)

            if ngram in selected_ngrams:
                selected_ngrams[ngram] = selected_ngrams[ngram] + 1
            else:
                selected_ngrams[ngram] = 1

            score = score + ng_score

        score = score * 1 / len(ngrams)
        column_sep = '\t'
        print('%s%s%s' % (line_clear, column_sep, score))
    f2.close


# python context_select_data.py init_corpus selection_file 1
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(sys.stderr, "Usage:", sys.argv[0], '[selected_file_init] [selection_file] [factor]')
        quit()

    separator_words = ' '

    selected_file_init = sys.argv[1]
    selection_file = sys.argv[2]
    factor = float(sys.argv[3])

    selected_ngrams = readDic(selected_file_init, separator_words)
    dict_all_ngrams = readDic(selection_file, separator_words)

    sentence_score(selection_file, factor, selected_ngrams, dict_all_ngrams, separator_words)

    # selected ngrams: 一句
    # dict_all_gram：所有文本
