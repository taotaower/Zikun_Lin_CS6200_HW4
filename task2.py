#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
from math import log

with open('1-gram.json', 'r') as f:
    tf = json.load(f)

idf ={}

for w in tf:
    idf[w] = len(tf[w])


query = raw_input("input '$end!' to stop, please enter your query input : ")
tQuery = list(query.split(' '))
queryID = 1
systemName = "ZikunLin's BM25"


while (tQuery != ['$end!']):
    qTerm = {}

    for t in tQuery:
        if qTerm.has_key(t):
            qTerm[t] +=1
        else:
            qTerm[t] = 1


    def readFolder(): # read the docs in the folder
        list_dirs = os.walk('cleanedDocs')
        for root, dirs, files in list_dirs:
            return files

    files = readFolder()
    files.pop(0)

    N = len(files)
    totalLen = 0
    for f in files:
        u = re.match(r'(.*?)(.txt)', f)
        path = 'cleanedDocs/' + f
        f = open(path, 'r')
        content = f.read()
        f.close()
        totalLen += len(content)
    avdl = totalLen / float(N)

    k1 = 1.2
    b = 0.75
    k2 = 100

    def bm25(qTerm,docID,K,N,idf,tf):
        score = 0
        for i in qTerm:

            if idf.has_key(i):
                ni = idf[i]
            else:
                ni = 0
            if tf.has_key(i):
                if tf[i].has_key(docID) :
                    fi = tf[i][docID]
                else:
                    fi = 0
            else:
                fi = 0
            qfi = qTerm[i]
            score += log(1/((ni + 0.5)/(N-ni + 0.5))) * (((k1 + 1) * fi)/(K + fi)) * (((k2 + 1)*qfi)/(k2 + qfi))
        return score
    scores = {}

    for f in files:
        u = re.match(r'(.*?)(.txt)', f)
        docID = u.group(1)
        path = 'cleanedDocs/' + f
        f = open(path, 'r')
        content = f.read()
        f.close()
        K = k1 * ((1 - b) + b * (len(content) / float(avdl)))
        score = bm25(qTerm,docID,K,N,idf,tf)
        scores[docID] = score

    scores = sorted(scores.iteritems(), key=lambda d: d[1], reverse=True)[0:100]
    print scores

    fobj = open('BM25.txt', 'a')
    firstLine = 'input query:' + query + '\n'
    fobj.write(firstLine)
    rank = 1
    for s in scores:
        line = str(queryID) + '   '+  'Q0 ' + s[0] + '   '+  str(rank) + '   ' + str(s[1]) + '   ' + systemName + '\n'
        fobj.write(line)
        rank +=1
    fobj.close()


    query = raw_input('please enter your query: ')
    tQuery = list(query.split(' '))
    queryID += 1



# kaolv