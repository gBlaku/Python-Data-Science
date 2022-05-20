import re
import math


def clean():
    originalFile = open('tfidf_docs.txt', 'r')
    files = originalFile.readlines()
    originalFile.close()
    record = {}
    for x in files:
        x_clean = x.strip()
        files[files.index(x)] = x_clean
        reader = open(files[files.index(x_clean)],'r')
        content = reader.read()    
        wordList = []
        for x in content.split():
            if 'http://' not in x and 'https://' not in x:
                wordList.append(re.sub('\W', '', x).lower())
        
        reader.close()
        record[x_clean] = wordList
        # record[x_clean] = ' '.join(wordList)
    return record
    
def remove_stopwords(record):
    file = open('stopwords.txt','r')
    stopwords = file.readlines()
    file.close
    for word in stopwords:
        wordClean = word.strip()
        stopwords[stopwords.index(word)] = wordClean
        for key in record:
            for word in record[key]:
                if word == wordClean or len(word) < 1:
                    record[key].remove(word)
    return record
    
def stemming_and_lemmatization(record):
    for key in record:
        for word in record[key]:
            rootForm = word
            if re.search('ing$', word):
                rootForm = re.sub('ing$', '', rootForm)
            elif re.search('ly$',rootForm):
                rootForm = re.sub('ly$', '',rootForm)
            elif re.search('ment$',rootForm):
                rootForm = re.sub('ment$','',rootForm)
            record[key][record[key].index(word)] = rootForm
    return record
    
def computeTF_IDF(record):
    wordFrequency = {
#         document : {word : frequency} 
    }
    TF = {
#         document : {word : TF}
    }
    IDF = {
#         document : {word : IDF}
    }
    totalTerms=  {}
#         document: num
    
    
    for key in record:
        if key not in wordFrequency:
            wordFrequency[key] = {}
        if key not in totalTerms:
            totalTerms[key] = 0
        for word in record[key]:
            totalTerms[key]+= 1
            if word in wordFrequency[key]:
                wordFrequency[key][word] += 1
            else:
                wordFrequency[key][word] = 1
    
    wordAppearance = {
        # word: docNum
    }
    
    for document in wordFrequency:
        for word in wordFrequency[document]:
            if word not in wordAppearance:
                wordAppearance[word] = 1
            else:
                wordAppearance[word] += 1
    
    for document in wordFrequency:
        TF[document]={}
        IDF[document]= {}
        for word in wordFrequency[document]:
            timesInDocument = wordFrequency[document][word]
            totalTermsInDocument = totalTerms[document]
            TF_score = timesInDocument/totalTermsInDocument
            
            TF[document][word] = TF_score
            
            totalNumDocument = len(totalTerms.keys())
            totalAppearances = wordAppearance[word]
            if totalAppearances == 0:
                continue
            else:
                IDF_score = math.log( (totalNumDocument/totalAppearances) ) + 1
                IDF[document][word]=IDF_score

    return TF, IDF


import re
import math

def main():
    record = clean()
    record = remove_stopwords(record)
    record = stemming_and_lemmatization(record)
    for key in record:
        with open('preproc_' + key, 'w') as f:
            f.write(' '.join(record[key]))
#     This here is the start of Part 2
    TF, IDF = computeTF_IDF(record)
    TF_IDF = {
#         document: {word: TF_IDF value}
    }
    for key in TF:
        TF_IDF[key] = {}
        for word in TF[key]:
            TF_IDF[key][word] = round(TF[key][word] * IDF[key][word] , 2)
    
 
    for key in TF_IDF:
        TF_IDF[key] = sorted(TF_IDF[key].items())
        TF_IDF[key] = sorted(TF_IDF[key], key=lambda x: x[1], reverse=True)
      
    
  #  print ( TF_IDF['doc1.txt'][0])
    
    for key in TF_IDF:
        file = open('tfidf_' + key, 'w')
        count = 0
        lst =[]
        for value in range(len(TF_IDF[key])):
            if count < 5:
               # print (''.join( str((TF_IDF[key][value]))) )
                lst.append((TF_IDF[key][value]))
                # file.write(''.join( str((TF_IDF[key][value]))))
                #file.write(str((TF_IDF[key][value])))
            count+=1
        lst = str(lst)
        file.write(lst)
        file.close()
            
    
    
main()