f = open('briefings.jsonl', 'r')

f = open('demo_seg1.csv', 'r')
import json
import string;
import nltk

from collections import defaultdict
from boltons.jsonutils import JSONLIterator
from boltons.dictutils import OMD
from lxml.html import soupparser
from lxml.cssselect import CSSSelector


BRIEFINGS_FILE = 'briefings.jsonl'
CITIES_FILE = 'cities.json'

def main():
    cities_json = json.load(open(CITIES_FILE))
    pop_cities = sorted(cities_json, lambda o, _: int(o['population']), reverse=True)
    # print pop_cities[:20]
    cities = [o['city'] for o in pop_cities][:20]
    jsonl_iter = JSONLIterator(open(BRIEFINGS_FILE))

    res = defaultdict(list)
    nums = 0;
    for obj in jsonl_iter:
        title = obj['title']
        briefing_html = obj['content']

        content_tree = soupparser.fromstring(briefing_html)
        pane_tree = content_tree.cssselect('.pane-node-field-forall-body')
        briefing_text = pane_tree[0].text_content()

        print "-------------------------"
        print title;
        print briefing_text;
        nums = nums +1;

        if nums > 3:
            break;

        for city in cities:
            if city in briefing_text:
                res[city].append(title)
                print 'found', repr(city), 'in', repr(title)

    omd = OMD()
    for k in res:
        omd.addlist(k, res[k])
    top_items = sorted(omd.counts().items(), key=lambda x: x[1], reverse=True)

    import pdb;pdb.set_trace()




###
def removeStopWords(Title):
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',
                       '/','//','<','>'])  # remove it if you need punctuation
    sizeWords = ['gr', 'percent', 'over', 'approx', 'pkg', 'capsul', 'kilo', 'gm', 'lbfrontier',
                 'ima', 'lb', 'jar', 'pouch', 'cup', 'calor', 'jak', 'pot', 'pack', 'multi', 'liter', 'pcs',
                 'piec', 'bar', 'gram', 'set', 'oun', 'weight', 'packet', 'btl', 'oz', 'ounc', 'per', 'categori',
                 'half', 'nbsp','also','bott', 'ca', 'gallon', 'fl', 'bags', 'box', 'packa','th','','w','lsdexcept']

    stop_words.update(sizeWords)

    outputTitle = "";
    TitleList = Title.split(' ')
    #TitleList = nltk.sent_tokenize(Title)
    for tit in TitleList:
        #print tit
        if tit.strip()  not in stop_words:
            outputTitle += tit + " "
        else:
            outputTitle = outputTitle;
    if len(outputTitle) > 1:
        outputTitle = outputTitle[0:(len(outputTitle)-1)];

    return outputTitle

###

import string;
import nltk
import json
import ast
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


f = open('/Users/simonkim/Documents/out_category_Data3.csv', 'r')
desc_list = f.read().split("\n")
descriptions = []


for desc in desc_list:
    descriptions.append(desc.split(" "))


descriptions1= descriptions
descriptions.remove(descriptions[len(descriptions ) -1])
desc_list.remove(desc_list[len(desc_list ) -1])

dictionary = corpora.Dictionary(descriptions)
type(dictionary.token2id)
raw_corpus2 = [dictionary.doc2bow(t.split(" ")) for t in desc_list]

lda = gensim.models.ldamodel.LdaModel(corpus=raw_corpus2, id2word=dictionary, num_topics=25, update_every=1, chunksize=10000, passes=1)

lda10 = gensim.models.ldamodel.LdaModel(corpus=raw_corpus2,
                                        id2word=dictionary, num_topics=10, update_every=1, chunksize=10000, passes=1)

lda15 = gensim.models.ldamodel.LdaModel(corpus=raw_corpus2,
                                        id2word=dictionary, num_topics=15, update_every=1, chunksize=10000, passes=1)


###

cities_json = json.load(open(CITIES_FILE))
pop_cities = sorted(cities_json, lambda o, _: int(o['population']), reverse=True)
# print pop_cities[:20]
cities = [o['city'] for o in pop_cities][:20]
jsonl_iter = JSONLIterator(open(BRIEFINGS_FILE))

res = defaultdict(list)
nums = 0;

for obj in jsonl_iter:
    title = obj['title']
    briefing_html = obj['content']

    content_tree = soupparser.fromstring(briefing_html)
    pane_tree = content_tree.cssselect('.pane-node-field-forall-body')
    briefing_text = pane_tree[0].text_content()

    print "-------------------------"
    print title;
    print briefing_text.split(" ");
    nums = nums + 1;

    if nums > 3:
        break;

stemmer = SnowballStemmer("english")
exclude = set(string.punctuation)
s = briefing_text
s = ''.join(ch for ch in s if ch not in exclude)
#nltk.word_tokenize(s.encode('utf-8').lower())
s1 = str(s.encode('utf-8')).translate(None, '0123456789').lower()
tokens = nltk.word_tokenize(s1)

stop_words = set(stopwords.words('english'))


output = []
for token in tokens:
    stemms = stemmer.stem(token.decode('utf8'));
    i = 0;
    for stopW in stop_words:
        if stemms in stopW:
            i += 1;

    if i == 0:
        output.append(str(stemms.encode('utf8')));




stemmer.stem(tr.decode('utf8'))



def makeInputDate(briefing_text):
    exclude = set(string.punctuation)
    s = briefing_text
    s = ''.join(ch for ch in s if ch not in exclude)
    # nltk.word_tokenize(s.encode('utf-8').lower())
    s1 = str(s.encode('utf-8')).translate(None, '0123456789').lower()
    tokens = nltk.word_tokenize(s1)

    stop_words = set(stopwords.words('english'))
    sizeWords = ['presid','mr','say','think','go','well','get','q','said','veri'
                 , 'jame', 'bradi','press','brief','room','pm','est','go','got'
                 , 'ive','g','weve', 'one', 'dont', 'doe', 'de', 'hes','would'
                 ,'ani','also']

    stop_words.update(sizeWords)

    output = []
    for token in tokens:

        try:
            stemms = stemmer.stem(token);

        except UnicodeDecodeError:
            stemms = "UnicodeDecodeError";

        i = 0;
        #for stopW in stop_words:
        try:
            if stemms in stop_words:
                i += 1;
            elif stemms in sizeWords:
                i += 1;

        except UnicodeDecodeError:
                i += 1;

        try:
            if i == 0 and stemms != "UnicodeDecodeError":
                output.append(str(stemms.encode('utf8')));
        except UnicodeDecodeError:
             i += 1;

    return output;




descriptions = []


##
cities_json = json.load(open(CITIES_FILE))
pop_cities = sorted(cities_json, lambda o, _: int(o['population']), reverse=True)
# print pop_cities[:20]
cities = [o['city'] for o in pop_cities][:20]
jsonl_iter = JSONLIterator(open(BRIEFINGS_FILE))

res = defaultdict(list)
nums = 0;
descriptions = []
for obj in jsonl_iter:
    title = obj['title']
    briefing_html = obj['content']

    content_tree = soupparser.fromstring(briefing_html)
    pane_tree = content_tree.cssselect('.pane-node-field-forall-body')
    briefing_text = pane_tree[0].text_content()
    descriptions.append(makeInputDate(briefing_text))
    nums += 1;
    print nums



##
from gensim import corpora, models, similarities
import logging, gensim, bz2
dictionary = corpora.Dictionary(descriptions)
type(dictionary.token2id)
raw_corpus2 = [dictionary.doc2bow(t) for t in descriptions]

lda = gensim.models.ldamodel.LdaModel(corpus=raw_corpus2, id2word=dictionary, num_topics=15, update_every=1, chunksize=50, passes=1)
lda.print_topics(15)
##
def removeStopWords(Title):
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',
                       '/','//','<','>'])  # remove it if you need punctuation
    sizeWords = ['presid','mr','say']

    stop_words.update(sizeWords)

    outputTitle = "";
    TitleList = Title.split(' ')
    #TitleList = nltk.sent_tokenize(Title)
    for tit in TitleList:
        #print tit
        if tit.strip()  not in stop_words:
            outputTitle += tit + " "
        else:
            outputTitle = outputTitle;
    if len(outputTitle) > 1:
        outputTitle = outputTitle[0:(len(outputTitle)-1)];

    return outputTitle


def getProb(ldaList):
    return ldaList[1];



cities_json = json.load(open(CITIES_FILE))
pop_cities = sorted(cities_json, lambda o, _: int(o['population']), reverse=True)
# print pop_cities[:20]
cities = [o['city'] for o in pop_cities][:20]
jsonl_iter = JSONLIterator(open(BRIEFINGS_FILE))

res = defaultdict(list)
nums = 0;

foutput = open('/Users/simonkim/Documents/obamatopic2.csv', 'w')
foutput.write("date, topic, prob, topic2, porb2, topic3, porb3" + "\n")
desc  = [];
for obj in jsonl_iter:
    title = obj['title']
    tt = title.split(",")
    #print tt
    ldaOutput = lda30[dictionary.doc2bow(descriptions[nums])]
    if len(ldaOutput) > 2:
        firstLda = sorted(ldaOutput, key=getProb, reverse=True)[0];
        secondLda = sorted(ldaOutput, key=getProb, reverse=True)[1];
        thirdLda = sorted(ldaOutput, key=getProb, reverse=True)[2];
    else:
        firstLda = sorted(ldaOutput, key=getProb, reverse=True)[0];
        secondLda = sorted(ldaOutput, key=getProb, reverse=True)[1];
        thirdLda = [-99,0]

    if len(tt) > 1 :
        outputs = str(tt[1]) + "," + str(firstLda[0]) + ", " + \
                  str(firstLda[1]) + ", " + \
                  str(secondLda[0]) +","+str(secondLda[1]) + "," + \
                  str(thirdLda[0]) +","+str(thirdLda[1]) + "\n"
    else:
        outputs = "None" + "," +\
                  str(firstLda[0]) + ", " + str(firstLda[1]) + ", " + \
                  str(secondLda[0]) +","+ str(secondLda[1]) + ", "+ \
                  str(thirdLda[0]) +","+str(thirdLda[1]) + "\n"

    #print outputs;

    if firstLda[0] == 18:
        desc.append(descriptions[nums]);

    foutput.write(outputs)

    nums += 1;
    #print nums

foutput.close()


dictionary1 = corpora.Dictionary(desc)
type(dictionary1.token2id)
raw_corpus3 = [dictionary1.doc2bow(t) for t in desc]

lda_1 = gensim.models.ldamodel.LdaModel(corpus=raw_corpus3, id2word=dictionary, num_topics=10, update_every=1, chunksize=15, passes=1)

import pyLDAvis.gensim
obama =  pyLDAvis.gensim.prepare(lda30, raw_corpus2,dictionary)
pyLDAvis.display(obama)

corpora.MmCorpus.serialize('raw_corpus2.mm',
                           raw_corpus2)
dictionary.save('obama.dic')
lda25.save("obama25.lda")

import gensim.models.phrases
bigram = gensim.models.Phrases(descriptions)
bigram[descriptions[0]]

descriptionsBiGram = [];
for sent in descriptions:
    descriptionsBiGram.append(bigram[sent])

dictionaryBiGram = corpora.Dictionary(descriptionsBiGram)
type(dictionaryBiGram.token2id)
raw_corpusBigram = [dictionaryBiGram.doc2bow(t) for t in descriptionsBiGram]

ldaBigram = gensim.models.ldamodel.LdaModel(corpus=raw_corpusBigram, id2word=dictionaryBiGram, num_topics=25, update_every=1, chunksize=25, passes=1)

corpora.MmCorpus.serialize('raw_corpusBigram2.mm',
                           raw_corpusBigram)
dictionaryBiGram.save('obamaBigram.dic')
ldaBigram.save("obamaBogram25.lda")

corpora.MmCorpus.serialize('raw_corpusBigram22.mm',
                           raw_corpusBigram)
dictionaryBiGram.save('obamaBigram2.dic')
ldaBigram.save("obamaBogram25_2.lda")


