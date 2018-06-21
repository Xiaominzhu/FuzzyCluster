# -*- coding:utf-8-*-
import jieba
jieba.load_userdict("F:/graduationThesis/dataSet/test/addDict.txt")

# 模糊形式背景的转置（对象:特征词，属性:文本id，关系：tf-idf值）
def contextTr(fpath, fpath_Tr):
    f = open(fpath, 'r')
    fwrite = open(fpath_Tr, 'w+')
    textList = []
    linenum = 0
    allwordstmp = []
    for line in f.readlines():
        linenum += 1
        lineList = line.strip(",\r\n").split(",")
        textList.append(lineList)
        for wdval in lineList:
            wd = wdval.split(":")[0]
            allwordstmp.append(wd)
    allwordsList = list(set(allwordstmp))
    for wd in allwordsList:
        for i in range(len(textList)):
            for elem in textList[i]:
                if(elem.split(":")[0] == wd):
                    fwrite.write(str(i) + ":")
                    fwrite.write(elem.split(":")[1] + ",")
        fwrite.write("\n")

def getInput_Tr(fpath_Tr, fpath_Tr_Input):
    fRead = open(fpath_Tr, 'r')
    fwrite = open(fpath_Tr_Input, 'w+')
    fwrite.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" + "\n")
    fwrite.write("<context uri=\"http://www.mia.com\">" + "\n")
    newsNums = 1
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

