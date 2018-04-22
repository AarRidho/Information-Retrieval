from pathlib import Path
p = Path('c:/Users/Aar/Desktop/Tugas TKI/corpus')
a = list(p.glob('**/*.txt'))
print(a)
tempCorpus = []
tempTexts = []

for s in a:  
    with s.open() as f:
        for line in f:
            tempTexts.append(line)
    tempCorpus.append(tempTexts)
    print(tempTexts)
    tempTexts = []
        
print(tempCorpus)
