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


#using textblob for additional filtering
bloblist = blobers(tempCorpus)


#queries
query = 'rumah anda saya dipecat istri motor'
query2 = 'istri anda di rumah'
query3 = 'rumah saya ada di tangerang selatan'
query4 = 'rumah aar ada istri'
query5 = 'istri aar di tilang'

queries = [query]
#queries = [query,query2,query3,query4,query5] #5 queries example

sheet=[]
#Stem and filters queries
for i,q in enumerate(queries):
    temp = stopword.remove(q)
    queries[i] = stemmer.stem(temp)

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
        print(idf)
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
            tf = blob.words.count(s)
            tfidf = tf*idf
            tempArrayQ.append(tfidf)
            
print(tempArrayQ)

print(countrs)  #counter for corpus list


#Cosine Similarities
#deploy to find dotProducts
def deploy(docNo):
    m = docNo-1
    total=0
    for i in range(len(tempArrayQ)):
        for x in range(countrs):
            if m==x:
                print(i+1,x+1,tempArrayQ[i],tempArray2[i][x],tempArrayQ[i]*tempArray2[i][x])
                total+=tempArrayQ[i]*tempArray2[i][x]
                break

    return total    

#deploy2 to find related document frequencies
def deploy2(docNo):
    n = docNo-1
    total = 0
    for x in range(len(tempArray2)):
        for i in range(countrs):
            if n==i:
                print(x+1,i+1, tempArray2[x][i])
                total+=tempArray2[x][i]**2
                break
    return total

dotTotal=0
qS = 0
dS = 0
cos=[]
#loop to find query frequencies
total=0
for x in tempArrayQ:
    total+=x**2

for a in range(countrs):
    print("\nD"+str(a))
    #this is Document 1 tf idf
    dotTotal+=deploy(a+1) #deploy(query, whichDoc) in this case we use query 1 and doc 1
    print("\ndot total "+str(dotTotal))
    #P.S you can control the deploy value to search through docs with defined queries before

    temp=[]
    
    qS = math.sqrt(total)
    dS = math.sqrt(deploy2(a+1))
    print("\n"+str(total))
    print("qs "+str(qS))
    print("ds "+str(dS))
    dotS = dotTotal/(qS*dS)

    #Cosine Similarity Result
    print("\n"+str(dotS))
    temp.append("D"+str(a+1))
    temp.append(dotS)
    cos.append(temp)
    temp=[]
    dotTotal=0

cos.sort(key=lambda x:x[1], reverse=True)
print(cos)
sheet.append("q1")
sheet.append(cos)


workbook = xlsxwriter.Workbook('cosine.xlsx')
worksheet = workbook.add_worksheet()
rowsheet = 0
col = 0

for x,i in enumerate(sheet):
    if(x==1):
        for d,c in enumerate(i):
            if(d==0):
                worksheet.write(rowsheet, d+1, str(c))
                rowsheet+=1
            else:
                worksheet.write(rowsheet, d, str(c))
                
    else:
        worksheet.write(rowsheet, col, str(i))

    
workbook.close()
        

