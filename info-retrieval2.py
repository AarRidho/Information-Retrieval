import math
import xlsxwriter
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


#Stemmed and filtered corpus right here
print(tempCorpus)



#queries
query = 'kontur tanah dan udara lebih baik'
query2 = 'istri anda di rumah'
query3 = 'rumah saya ada di tangerang selatan'
query4 = 'rumah aar ada istri'
query5 = 'istri aar di tilang'

queries = [query]
#queries = [query,query2,query3,query4,query5] #5 queries example

#using textblob for additional filtering
bloblist = blobers(tempCorpus)
bloblistquery = blobers(queries)

sheet=[]
#Stem and filters queries
for i,q in enumerate(queries):
    temp = stopword.remove(q)
    queries[i] = stemmer.stem(temp)

tempArrayTF = []
tempArray2 = []
tempIdf = []
tempIdf2 = []

for i, blobs in enumerate(bloblistquery):
    for x,blobd in enumerate(bloblist):
        scores = {s: tfidf(s, blobd, bloblist) for s in blobs.words}
        sorted_words = scores.items()
        print("D"+str(x+1))
        for word, score in sorted_words:
            print("\tWord: {}, TF-IDF: {}".format(word, score))
    

