#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import MeCab as mc
import re
import numpy as np

def mecab_analysis(text):
    t = mc.Tagger("-Ochasen")
    node = t.parseToNode(text) 
    sentence = []
    output = []
    while node:
        sentence.append(node.surface)        
        if node.surface == "\n\n":
            output.append(sentence)
            sentence = []
    return output


def get_freqdict(sentences):
    freqdict = {}
    N = 0
    for sentence in sentences:
        for word in sentence:
            freqdict.setdefault(word, 0.)
            freqdict[word] += 1
            N += 1
    return freqdict

def score(sentence, freqdict):
    return np.sum([np.log(freqdict[word]) for word in sentence]) / len(sentence)

def direct_proportion(i, n):
    return float(n-i+1)/n

def inverse_proportion(i, n):
    return 1.0 / i

def geometric_sequence(i, n):
    return 0.5 ** (i-1)

def inverse_entropy(p):
    if p == 1.0 or 0.0:
        return 1.0
    return 1-(-p*np.log(p) - (1-p)*np.log(1-p))

def inverse_entropy_proportion(i, n):
    p = i / n
    return inverse_entropy(p)

def summarize(text, limit=100, **options):
    """
    text: target text
    limit: summary length limit
    option: 
    -m: summarization mode
        0: basic summarization model
        1: using word position feature
    -f: feature function
        0: direct proportion (DP)
        1: inverse proportion (IP)
        2: Geometric sequence (GS)
        3: Binary function (BF)
        4: Inverse entropy 
    """
    sentences = mecab_analysis(text)
    freqdict = get_freqdict(sentences)
    if options["m"] == 0:
        scores = [score(sentence, freqdict) for sentence in sentences]
    if options["m"] == 1:
        if options["f"] == 0:
            word_features = direct_proportion
        elif options["f"] == 1:
            word_features = inverse_proportion
        elif options["f"] == 2:
            word_features = geometric_sequence
        elif options["f"] == 4:
            word_features = inverse_entropy_proportion

        scores = []
        feature_dict = {}
        for sentence in sentences:
            sent_score = 0.0
            for word in sentence:
                feature_dict.setdefault(word, 0.0)
                feature_dict[word] += 1
                sent_score += np.log(freqdict[word]) * word_features(feature_dict[word], freqdict[word])
            sent_score /= len(sentence)
            scores.append(sent_score)

    topics = []
    length = 0
    for index in sorted(range(len(scores)), key=lambda k: scores[k], reverse=True):
        length += len(sentences[index])
        if length > limit: break
        topics.append(index)
    topics = sorted(topics)
    return "".join(["".join(sentences[topic]) for topic in topics])


def main():
    blog_title = u"けやかけのお話し.txt"
    blog_text = open(blog_title).read()
    print(blog_title)
    print("=====================================================")
    print(blog_text)
    print(summarize(blog_text, m=1, f=0))

if __name__ == '__main__':
    main()


