import sys
import os
import nltk
from collections import Counter
import collections
from nltk import word_tokenize
from nltk.util import ngrams
import random

finalwords = []
finalpath=sys.argv[1]
replacewords=open('EnglishStopwords.txt').read().split()
fileprobailities=sys.argv[2]
fileresults=sys.argv[3]

for x in os.walk(finalpath):
    for j in x[2]:
        if j.endswith('.txt'):
            f = open(os.path.join(finalpath,j),encoding="utf8")
            finalwords.append(f.read().lower().split())
countofwords = Counter([])

for wordvalues in replacewords:
    for x in range(len(finalwords)):
        for book in finalwords[x]:
            if( wordvalues == book):
                finalwords[x].remove(wordvalues)

for x in range(len(finalwords)):
    for book in finalwords[x]:
        value = nltk.word_tokenize(book)
        u_unigrams = ngrams(value, 1)
        b_bigrams = ngrams(value, 2)
        t_trigrams = ngrams(value, 3)
        countofwords += Counter(u_unigrams)

listofwords = ' '.join(finalwords[1])
words = listofwords.split()
bigrammappp  = collections.defaultdict(dict)
bigramcounter = collections.defaultdict(int)
unigrammapp = collections.defaultdict(dict)
unigramcounter = collections.defaultdict(int)

for a,b,c in zip(words,words[1:],words[2:]):
  a,b,c = a.lower(),b.lower(),c.lower()
  bigram = a+' '+b  
  if bigram not in bigrammappp:
    bigrammappp[bigram] = {}
  bigrammappp[bigram][c] = bigrammappp[bigram].get(c,0)+1
  bigramcounter[bigram]+=1
 
for a,b in zip(words,words[1:]):
  a,b = a.lower(),b.lower()
  unigram = a  
  if unigram not in unigrammapp:
    unigrammapp[a] = {}
  unigrammapp[unigram][b] = unigrammapp[unigram].get(b,0)+1
  unigramcounter[unigram]+=1
  
  
def caluculatingbigramprobs(bigram,wordvalues,bigrammappp,bigramcounter):
  if bigram not in bigrammappp or wordvalues not in bigrammappp[bigram]:
    return 0  
  
  deno = bigramcounter[bigram]
  numo = bigrammappp[bigram][wordvalues]
  return numo/deno


def calculateunigramprobs(unigram,wordvalues,unigrammapp,unigramcounter):
  if unigram not in unigrammapp or wordvalues not in unigrammapp[unigram]:
    return 0  
  deno = unigramcounter[unigram]
  numo = unigrammapp[unigram][wordvalues]
  return numo/(deno*1.0)


def probsofunigrams(unigramcounter,unigram,length):
    if unigram not in unigramcounter:
        return 0
    else:
        return unigramcounter[unigram]/(length*1.0)
    
lengthofwords=len(finalwords[0])+len(finalwords[1])+len(finalwords[2])
print(unigramcounter)
print("over here")
counter = 0

dictkeys =  list(unigramcounter.keys())
filevalues= open(fileprobailities, "w",encoding='utf-8')
for key in dictkeys:
    value = unigramcounter[key]
    d=probsofunigrams(unigramcounter,key,lengthofwords)
    m=str(key)+" "+str(d)+"\n"
    filevalues.write(m)
filevalues.write("*************************Conditional_Unigram*****************************************")

for k1 in dictkeys:
  for k2 in dictkeys:
    if k1 !=k2:
      d=calculateunigramprobs(k1,k2,unigrammapp,unigramcounter)
      if d:
        m=str(k1)+" "+str(k2)+" "+str(d)+"\n"
        filevalues.write(m)

filevalues.write("*************************Conditional _Bigram*****************************************")

bigram_keys = list(bigrammappp.keys())
for k1 in bigram_keys:
  for k2 in dictkeys:
    d=caluculatingbigramprobs(k1,k2,bigrammappp,bigramcounter)
    if d:
      m=str(k1)+" "+str(k2)+" "+str(d)+"\n"
      filevalues.write(m)

new_corpus=random.sample(dictkeys, 20)

random_sequence = []
for _ in range(10):
  random_sequence+=random.sample(dictkeys,20)

def do_everything(file_name,finalwords):
  listofwords = ' '.join(finalwords)
  words = listofwords.split()
  bigrammappp  = collections.defaultdict(dict)
  bigramcounter = collections.defaultdict(int)
  unigrammapp = collections.defaultdict(dict)
  unigramcounter = collections.defaultdict(int)

  for a,b,c in zip(words,words[1:],words[2:]):
    a,b,c = a.lower(),b.lower(),c.lower()
    bigram = a+' '+b  
    if bigram not in bigrammappp:
      bigrammappp[bigram] = {}
    bigrammappp[bigram][c] = bigrammappp[bigram].get(c,0)+1
    bigramcounter[bigram]+=1
    
    
  for a,b in zip(words,words[1:]):
    a,b = a.lower(),b.lower()
    unigram = a  
    if unigram not in unigrammapp:
      unigrammapp[a] = {}
    unigrammapp[unigram][b] = unigrammapp[unigram].get(b,0)+1
    unigramcounter[unigram]+=1
    
    
  def caluculatingbigramprobs(bigram,wordvalues,bigrammappp,bigramcounter):
    if bigram not in bigrammappp or wordvalues not in bigrammappp[bigram]:
      return 0  
    
    deno = bigramcounter[bigram]
    numo = bigrammappp[bigram][wordvalues]
    return numo/(deno*0.1)


  def calculateunigramprobs(unigram,wordvalues,unigrammapp,unigramcounter):
    if unigram not in unigrammapp or wordvalues not in unigrammapp[unigram]:
      return 0  
    deno = unigramcounter[unigram]
    numo = unigrammapp[unigram][wordvalues]
    return numo/(deno*1.0)


  def probsofunigrams(unigramcounter,unigram,length):
      if unigram not in unigramcounter:
          return 0
      else:
          return unigramcounter[unigram]/(length*1.0)
      
  lengthofwords=len(finalwords)

  dictkeys =  list(unigramcounter.keys())
  filevalues= open(file_name, "a",encoding='utf-8')
  for key in dictkeys:
      value = unigramcounter[key]
      d=probsofunigrams(unigramcounter,key,lengthofwords)
      m=str(key)+" "+str(d)+"\n"
      filevalues.write(m)
  filevalues.write("*************************unigram_conditional_values*****************************************")

  for k1 in dictkeys:
    for k2 in dictkeys:
      if k1 !=k2:
        d=calculateunigramprobs(k1,k2,unigrammapp,unigramcounter)
        if d:
          m=str(k1)+" "+str(k2)+" "+str(d)+"\n"
          filevalues.write(m)
  filevalues.write("*************************Bigram_conditional_values*****************************************")
  bigram_keys = list(bigrammappp.keys())
  for k1 in bigram_keys:
    for k2 in dictkeys:
      d=caluculatingbigramprobs(k1,k2,bigrammappp,bigramcounter)
      if d:
        m=str(k1)+" "+str(k2)+" "+str(d)+"\n"
        filevalues.write(m)
        
#20 tokens and 10 seqences random generation.
for iteration in range(10):
  do_everything(fileresults,random_sequence[iteration])
  print("completed sequence "+str(iteration))

filevalues.close()
