#!/usr/bin/env python
#-*- coding: utf8 -*-

from nltk.tag.stanford import POSTagger, NERTagger
import sys, getopt, argparse, tempfile, os

# POSTagger settings
model = '/opt/stanford-postagger/models/german-fast-caseless.tagger'
postagger = '/opt/stanford-postagger/stanford-postagger.jar'
st = POSTagger(model, postagger, 'utf-8')

# NERTagger settings
classifier = '/opt/stanford-ner/classifiers/hgc_175m_600.crf.ser.gz'
ner = '/opt/stanford-ner/stanford-ner.jar'
nt = NERTagger(classifier, ner, 'utf-8')

# Parse arguments
parser = argparse.ArgumentParser(description='German word tagging script by Sebastjanas Vaisovas')
parser.add_argument('-i','--input', help='Input filename',required=True)
parser.add_argument('-o','--output', help='Output filename',required=True)
args = parser.parse_args()

# Reading file contents to string
sentences = open(str(args.input)).read()

# Tagging content
output_st = st.tag(sentences.split())

text = ""

# Capitalizing words. Tag table: http://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/TagSets/stts-table.html

with tempfile.NamedTemporaryFile(delete=False) as f, open(args.output,'w') as o:
    for i in output_st:
        w, t = i
        if (t == "NN" or t == "NE" or t == "XY" or t == "ADJD"):
            f.write((w.capitalize()+' ').encode('utf-8'))
        else:
            f.write((w+' ').encode('utf-8'))
    f.flush()
    sentences = open(str(f.name)).read()
    output_nt = nt.tag(sentences.split())
    for i in output_nt:
        w, t = i
        if t != ('O').decode('utf-8'):
            o.write((w.capitalize()+' ').encode('utf-8'))
        else:
            o.write((w+' ').encode('utf-8'))
    os.remove(f.name)
