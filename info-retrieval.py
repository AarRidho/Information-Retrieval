import math
import xlsxwriter
import operator
from textblob import TextBlob as tb
from pathlib import Path
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

#Corpus Path
p1 = Path('./corpus')
a = list(p1.glob('**/*.txt'))
countrs = sum(1 for i in a)

#Stopwords Path
p2 = Path('./stopwords/stopword_list_tala.txt')

#Factories
stemFactory = StemmerFactory()
stemmer = stemFactory.create_stemmer()

stopFactory = StopWordRemoverFactory()
stopword = stopFactory.create_stop_word_remover()

tempCorpus = []
tempTexts = ""
tempStopWords = []

with p2.open() as f:
    for line in f:
        tempLine = line.strip('\n')
        tempStopWords.append(tempLine)

for s in a:  
    with s.open() as f:
        for line in f:
            stopOutput = stopword.remove(line)
            stemOutput = stemmer.stem(stopOutput)
            print(stemOutput)
            tempTexts += ' ' + stemOutput
    tempCorpus.append(tempTexts)
    tempTexts = ""

def stopWordRemover(word, lib):
    temp = word.split()

    for s in lib:
        for i in temp:
            if s==i:
                temp.remove(s)
            
    return ' '.join(temp)

def blobers(docs):
    temp = []
    for s in docs:
        temp.append(tb(s))

    return temp

def tf(word, blob):
    return blob.words.count(word)/len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def vector(arr):
    temp = 0
    for i in arr:
        temp+=(i**2)

    return temp

def safe_abs(x):
    if(x==0):
        return 0
    else:
        return abs(x)

def safe_div(x,y):
    if y==0:
        return 0
    return x/y

#Stemmed and filtered corpus right here
print(tempCorpus)

#queries
#query = 'kontur tanah dan udara lebih baik'
#query = 'Universitas terbaik di Indonesia'
#query = 'Persija Jakarta berhasil lolos'
#query = 'sekolah menengah kejuruan di jakarta'
query = 'Perkembangan teknologi informasi'

queries = [query]

#using textblob for additional filtering
bloblist = blobers(tempCorpus)
bloblistquery = blobers(queries)

sheet=[]

#Stem and filters queries
for i,q in enumerate(queries):
    temp = stopword.remove(q)
    queries[i] = stemmer.stem(temp)

tempTFIDF = []
tempTFIDFArray = []     #1
tempTFIDFquery = []
tempTFIDFqueryA = []    #2
tempcos = []

#TFIDF Documents
for i, blobs in enumerate(bloblistquery):
    for x,blobd in enumerate(bloblist):
        scores = {s: tfidf(s, blobd, bloblist) for s in blobs.words}
        sorted_words = scores.items()
        print("\n\tD"+str(x+1)+":")
        tempArr = []
        for word, score in sorted_words:
            print("\tWord: {}, TF-IDF: {}".format(word, score))
            tempArr.append(score)

        tempTFIDFArray.append(tempArr)
        tempTFIDF.append(scores)

print(tempTFIDF)
print(tempTFIDFArray)

#TFIDF Query
for i, blobs in enumerate(bloblistquery):
    for x,blobd in enumerate(bloblist):
        scores = {s: tfidf(s, blobs, bloblist) for s in blobs.words}
        sorted_words = scores.items()
        print("Q"+str(x+1)+":")
        tempArr = []
        for word, score in sorted_words:
            print("\tWord: {}, TF-IDF: {}".format(word, score))
            tempTFIDFqueryA.append(score)

        tempTFIDFquery.append(scores)
        break
            
print(tempTFIDFquery)
print(tempTFIDFqueryA)

#cosine similarity
for y,scd in enumerate(tempTFIDFArray):
    temp=0
    for z,scz in enumerate(scd):
        temp+=(tempTFIDFqueryA[z]*scz)

    vectorQ = safe_abs(math.sqrt(vector(tempTFIDFqueryA)))
    vectorD = safe_abs(math.sqrt(vector(scd)))
    
    print("\nDotProduct(Q, D"+str(y)+"):"+str(temp))
    print("\nvectorQ: "+str(vectorQ))
    print("\nvectorD: "+str(vectorD))

    cos=safe_div(temp,(vectorQ*vectorD))
    print("Cos(Q, D1):"+str(cos))
    tempcos.append(cos)
    
print(tempcos)  

tempLastDict = {}

for i,x in enumerate(tempcos):
    tempLastDict["D"+str(i+1)] = x

print(tempLastDict)

_excel = sorted(tempLastDict.items(), key=operator.itemgetter(1),reverse=True)
print(_excel)

workbook = xlsxwriter.Workbook('cosineq5.xlsx')
worksheet = workbook.add_worksheet()

row=0
col=0

for doc, cos in _excel:
    worksheet.write(row, col, doc)
    worksheet.write(row, col+1, cos)
    row +=1

workbook.close()
