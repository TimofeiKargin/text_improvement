#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import numpy as np
import re

[sample_filename, terms_filename] = sys.argv[1:3]

def normalize_string(s, soft=False):
    s = s.lower().strip()
    s = re.sub(r"'m", r" am", s)
    s = re.sub(r"'s", r" is", s)
    s = re.sub(r"n't", r" not", s)
    s = re.sub(r"'ll", r" will", s)
    s = re.sub(r"'re", r" are", s)
    s = re.sub(r"'ve", r" have", s)
    if not soft:
        s = re.sub(r"[^a-zA-Z]+", r" ", s)
    return s

def create_terms_bi_vecs(terms):
    terms_bi_vecs = []
    for term in terms:
        pair = term.split()
        if len(pair) == 2:
            terms_bi_vecs.append(pair)
    
    terms_bi_vecs = list(map(lambda x: [[x[0], x[1]], [gl_dict[x[0]], gl_dict[x[1]]]], terms_bi_vecs))
    return terms_bi_vecs

def create_terms_tri_vecs(terms):
    terms_tri_vecs = []
    for term in terms:
        tri = term.split()
        if len(tri) == 3:
            terms_tri_vecs.append(tri)
    
    terms_tri_vecs = list(map(lambda x: [[x[0], x[1], x[2]], [gl_dict[x[0]], gl_dict[x[1]], gl_dict[x[2]]]], terms_tri_vecs))
    return terms_tri_vecs

def find_bigrams(s):
    b_list = []
    s = s.split()
    for i in range(len(s)-1):
        b_list.append([[s[i], s[i+1]], [gl_dict[s[i]], gl_dict[s[i+1]]]])
    return b_list

def find_trigrams(s):
    t_list = []
    s = s.split()
    for i in range(len(s)-2):
        t_list.append([[s[i], s[i+1], s[i+2]], [gl_dict[s[i]], gl_dict[s[i+1]], gl_dict[s[i+2]]]])
    return t_list

def cosine_similarity(a, b):
    nominator = np.dot(a, b)

    a_norm = np.sqrt(np.sum(a**2))
    b_norm = np.sqrt(np.sum(b**2))

    denominator = a_norm * b_norm

    cosine_similarity = nominator / denominator

    return cosine_similarity

def find_bi_sim(bigrams, terms_bi_vecs, thresh):
    ans = []
    for bigram in bigrams:
        for terms_bi_vec in terms_bi_vecs:
            avg_sim = 0
            for i in range(2):
                avg_sim += cosine_similarity(bigram[1][i], terms_bi_vec[1][i])
            avg_sim /= 2
            if avg_sim >= thresh:
                ans.append([bigram[0], terms_bi_vec[0]])
    return ans

def find_tri_sim(trigrams, terms_tri_vecs, thresh):
    ans = []
    for trigram in trigrams:
        for terms_tri_vec in terms_tri_vecs:
            avg_sim = 0
            for i in range(3):
                avg_sim += cosine_similarity(trigram[1][i], terms_tri_vec[1][i])
            avg_sim /= 3
            if avg_sim >= thresh:
                ans.append([trigram[0], terms_tri_vec[0]])
    return ans

def add_sugg(text, bi_sim, tri_sim):
    for tri in tri_sim:
        src_tri = ' '.join(tri[0])
        tgt_tri = ' '.join(tri[1])
        text = text.replace(src_tri, '{' + src_tri + ' -> ' + tgt_tri + '}')
    for bi in bi_sim:
        src_bi = ' '.join(bi[0])
        tgt_bi = ' '.join(bi[1])
        text = text.replace(src_bi, '{' + src_bi + ' -> ' + tgt_bi + '}')
    return text

glove_file = "./glove.6B.50d.txt"
glove_ar = "./glove.6B.50d.txt.zip"
if not os.path.isfile(glove_file):
    shutil.unpack_archive(glove_ar, './')
with open(glove_file, "r") as f:
    gl = f.readlines()
gl = list(map(lambda x: x[:-1], gl))

gl_dict = dict()
for i in range(len(gl)):
    split_gl = gl[i].split()
    gl_dict[split_gl[0]] = np.array(split_gl[1:]).astype('float64')

with open(sample_filename, "r") as f:
    sample_text = f.read()
sample_text_norm = normalize_string(sample_text)
sample_text_norm_soft = normalize_string(sample_text, soft=True)

with open(terms_filename, "r") as f:
    terms = f.readlines()
terms = list(map(lambda x: normalize_string(x.strip()), terms))

terms_bi_vecs = create_terms_bi_vecs(terms)
terms_tri_vecs = create_terms_tri_vecs(terms)

bigrams = find_bigrams(sample_text_norm)
trigrams = find_trigrams(sample_text_norm)

thresh = 0.67
tri_sim = find_tri_sim(trigrams, terms_tri_vecs, thresh)

thresh = 0.7
bi_sim = find_bi_sim(bigrams, terms_bi_vecs, thresh)

result = add_sugg(sample_text_norm_soft, bi_sim, tri_sim)
print(result)