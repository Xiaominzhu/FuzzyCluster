# -*- coding:utf-8-*-
from jieba import analyse
import jieba
jieba.load_userdict("F:/graduationThesis/dataSet/test/addDict.txt")

usenature = ("Ag","an","b","dg","g","h","i",
          "j","k","l","Ng","n","nr","ns","nt","nz",
          "s","tg","t","vg","vd","vn","x","z",
          "un")

#分词 并基于tfidf提取特征词
def jiebaSe(featureNums, fPath):
    f = open('F:/graduationThesis/dataSet/corpus4_sougou/sports.txt', 'r')
    fwrite = open(fPath, 'w+')
    keyWordsSet = set()
    linenums = 1
    lines = f.readlines()
    for i in range(18000, len(lines)):
        if(linenums >= 2000):
            break
        line = lines[i]
        linenums += 1
        analyse.set_stop_words("F:/graduationThesis/dataSet/test/stopWords.txt")
        seg_list = analyse.extract_tags(line, topK = featureNums, withWeight=True, allowPOS=usenature)
        for i in range(len(seg_list)):
            keyWordsSet.add(seg_list[i][0].encode('utf-8'))
            fwrite.write(seg_list[i][0].encode('utf-8') + ":" + str(round(seg_list[i][1], 2)) + ",")
        fwrite.write("\n")
    return list(set(keyWordsSet))

#将特征词对应的tfidf值进行归一化
def normalization(fPath, fPathNor):
    f = open(fPath, 'r')
    fwrite = open(fPathNor, 'w+')
    for line in f.readlines():
        lineList = line.strip(",\r\n").split(",")
        valList = []
        for valstr in lineList:
            valList.append(float(valstr.split(":")[1]))
        sumval = sum(valList)
        for valwrite in lineList:
            word = valwrite.split(":")[0]
            normvalue = round(float(valwrite.split(":")[1])/sumval, 2)
            fwrite.write(word + ":" + str(normvalue) + ",")
        fwrite.write("\n")

def getInput(fPathNor, fPathNor_Input):
    fRead = open(fPathNor, 'r')
    fwrite = open(fPathNor_Input, 'w+')
    fwrite.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" + "\n")
    fwrite.write("<context uri=\"http://www.mia.com\">" + "\n")
    newsNums = 0
    for line in fRead.readlines():
        fwrite.write("    <object name=\"" + str(newsNums) + "\">" + "\n")
        newsNums += 1
        wordList = line.strip(",\r\n").split(",")
        for wordValue in wordList:
            word = wordValue.split(":")[0]
            value = wordValue.split(":")[1]
            fwrite.write("        <attribute name=\"" + word + "\">" + "\n")
            fwrite.write("            <membership>" + value + "</membership>" + "\n")
            fwrite.write("        </attribute>" + "\n")
        fwrite.write("    </object>" + "\n")
    fwrite.write("</context>" + "\n")



