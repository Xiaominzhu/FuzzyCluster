# -*- coding:utf-8-*-

from __future__ import division
import xlrd
from jieba import analyse
import jieba
jieba.load_userdict("F:/graduationThesis/dataSet/test/addDict.txt")
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

usenature = ("Ag","an","b","dg","g","h","i",
          "j","k","l","Ng","n","nr","ns","nt","nz",
          "s","tg","t","vg","vd","vn","x","z",
          "un")

def typewordsDic():
    systempath = "F:/graduationThesis/dataSet/test/classificationSystem/sports_3L.xlsx"
    fsystem = xlrd.open_workbook(systempath)
    sheet1 = fsystem.sheet_by_name('Sheet1')
    nrows = sheet1.nrows   # sheet的行数，列数
    typewords = {}
    classlist = []
    for i in range(1, nrows):
        rowcontent = sheet1.row_values(i)
        class1 = rowcontent[1]
        classwords = rowcontent[2]
        typewords[class1] = classwords.split(";")
        classlist.append(class1)
    return typewords, classlist

def headMatch(typewords, classlist):
    resultWrite = open("F:/graduationThesis/dataSet/test/classifiByThreeConcepts/"
                       "result.txt", 'w+')
    fcorpus4 = open('F:/graduationThesis/dataSet/corpus4_sougou/sports.txt', 'r')
    path = 'F:/graduationThesis/dataSet/test/classifiByThreeConcepts/traindata3/'
    # fjb = 'F:/graduationThesis/dataSet/test/classifiByThreeConcepts/traindata/'
    # fwritejb = open(fjb, 'w+')
    # fnot = 'F:/graduationThesis/dataSet/test/classifiByThreeConcepts/traindata/classinot_sports_title.txt'
    # fwritenot = open(fnot, 'w+')
    # fjbnot = 'F:/graduationThesis/dataSet/test/classifiByThreeConcepts/traindata/classinot_jieba_title.txt'
    # fwritejbnot = open(fjbnot, 'w+')
    classnumsDic = {}
    stopwordpath = "F:/graduationThesis/dataSet/test/stopWords.txt"
    for wd in classlist:
        classnumsDic[wd] = 0
    analyse.set_stop_words(stopwordpath)   # 加载停用词
    nums = 0
    alllinenums = 0
    noclass = 0
    for line4 in fcorpus4.readlines():    # 将news的关键词与分类体系关键词进行匹配
        if(nums %100 == 0):
            print nums
        nums += 1
        alllinenums += 1
        line4list = line4.strip("\r\n").split(" title ")
        title = line4list[0]
        content = line4list[1]
        seg_title = list(jieba.cut(title, cut_all=False))
        seg_content = analyse.extract_tags(content, topK = 7, allowPOS=usenature)
        flag = 0
        for key, words in typewords.iteritems():
            if (contain_re(set(seg_content), set(words)) or
                    contain_re(set(seg_title), set(words))):
            # if (contain_re(set(seg_title), set(words))):
                path_text = path + str(key).decode('utf-8') + '.txt'
                fwrite = open(path_text, 'a+')
                fwrite.write(key + ":::" + line4)
                classnumsDic[key] = classnumsDic[key] + 1
                flag = 1
                # for w1 in seg_title:
                #     fwritejb.write(w1 + " ")
                # fwritejb.write("//")
                # for w2 in seg_content:
                #     fwritejb.write(w2 + " ")
                # fwritejb.write("\n")
        if(flag == 0):
            # fwritenot.write(line4)
            noclass += 1
        #     for w3 in seg_title:
        #         fwritejbnot.write(w3 + " ")
        #     fwritejbnot.write("//")
        #     for w4 in seg_content:
        #         fwritejbnot.write(w4 + " ")
        #     fwritejbnot.write("\n")
    resultWrite.write("noclass nums: " + str(noclass) + "\n")
    resultWrite.write("alllinenums: " + str(alllinenums) + "\n")
    resultWrite.write("noclass rate: " + str(noclass/alllinenums) + "\n")
    resultWrite.write("class rate: " + str(1 - noclass/alllinenums) + "\n")
    resultWrite.write("*********************" + "\n")
    for k, n in classnumsDic.items():
        resultWrite.write("class: " + str(k) + "\n")
        resultWrite.write("class nums: " + str(n) + "\n")
        resultWrite.write("class rate: " + str(int(n)/(alllinenums - noclass)) + "\n")

def contain_re(seg_set, wordsSet):
    for wd in seg_set:
        if(wd in wordsSet):
            return True
    return False

if __name__ == "__main__":
    typewords, classlist = typewordsDic()
    headMatch(typewords, classlist)


