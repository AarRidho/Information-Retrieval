import math
from textblob import TextBlob as tb
from pathlib import Path
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#Corpus Path
p1 = Path('./corpus')
a = list(p1.glob('**/*.txt'))
countrs = sum(1 for i in a)

#Stopwords Path
p2 = Path('./stopwords/stopword_list_tala.txt')

#Factories
stemFactory = StemmerFactory()
stemmer = stemFactory.create_stemmer()

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
            stemOutput = stemmer.stem(line)
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

for i in range(len(tempCorpus)):
    tempCorpus[i] = stopWordRemover(tempCorpus[i],tempStopWords)

print(tempCorpus)

bloblist = blobers(tempCorpus)

query = 'rumah anda saya dipecat istri'
query2 = 'istri anda di rumah'
query3 = 'rumah saya ada di tangerang selatan'
query4 = 'rumah aar ada istri'
query5 = 'istri aar di tilang'

queries = [query]
#queries = [query,query2,query3,query4,query5]

for i,q in enumerate(queries):
    queries[i] = stemmer.stem(q)

tempArray = []
tempArray2 = []
tempIdf = []
tempIdf2 = []
for q in queries:
    print('\nquery:', q)
    qsplit = q.split()
    for x,s in enumerate(qsplit):
        counter = 0
        idf = sum(1 for blob in bloblist if s in blob.words)
        idf = math.log(len(bloblist)/1 + idf)
        tempIdf.append(idf)
        print('idf(', s,'): ', idf)
        print(s,'\ntf:')
        for i, blob in enumerate(bloblist):
            print('total words', sum(1 for word in blob.words))
            print('D',i+1,': ', blob.words.count(s),', tf.idf: ', blob.words.count(s)*idf)
            tempArray.append(blob.words.count(s)*idf)
            counter += blob.words.count(s)
        tempArray2.append(tempArray)
        tempArray = []
        print('tftotal(', s,'): ', counter)
        print('\n')
    print('\n')
    tempIdf2.append(tempIdf)

print(tempArray2,'\n')

tempArrayQ = []         #query tf.idf
tempArrayQ2 = []
bloblistquery = blobers(queries)
for q in queries:
    qsplit = q.split()
    for x,s in enumerate(qsplit):
        idf = sum(1 for blob in bloblist if s in blob.words)
        idf = math.log(len(bloblist)/1 + idf)
        for i, blob in enumerate(bloblistquery):
            totalwords = sum(1 for word in blob.words)
            tf = blob.words.count(s)/sum(1 for word in blob.words)
            tfidf = tf*idf
            tempArrayQ.append(tfidf)
            
print(tempArrayQ)
print(countrs)

dotProduct = []

def deploy(queryNo, docNo):
    n = queryNo-1
    m = docNo-1
    for i in range(len(tempArrayQ)):
        for x in range(countrs):
            if n==i and m==x:
                print(i+1,x+1,tempArrayQ[i],tempArray2[i][x],tempArrayQ[i]*tempArray2[i][x])
                return tempArrayQ[i]*tempArray2[i][x]

def deploy2(docNo):
    n = docNo-1
    total = 0
    for x in range(len(tempArray2)):
        for i in range(countrs):
            if n==i:
                print(x+1,i+1, tempArray2[x][i])
                total+=tempArray2[x][i]*tempArray2[x][i]
                break
    return total

dotTotal=0
qS = 0
dS = 0
for x in range(countrs):
    dotTotal+=deploy(1,x+1)

total=0
for x in tempArrayQ:
    total+=x*x

qS = math.sqrt(total)
dS = math.sqrt(deploy2(1))
print(dS)
dotS = dotTotal/(qS*dS)

print(dotS)
        

