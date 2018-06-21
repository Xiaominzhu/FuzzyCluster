# -*- coding:utf-8-*-
from constructtraindataset import headmatch
classtheld = 500

def TrainData(classlist):
    ftraincorpus = open('F:/graduationThesis/dataSet/test/classifiByThreeConcepts'
                        '/classitrain_sports_title.txt', 'r')
    ft = 'F:/graduationThesis/dataSet/test/classifiByThreeConcepts/traindata_sports.txt'
    fwrite = open(ft, 'w+')
    classnums = {}
    for wd in classlist:
        classnums[wd.encode("utf-8")] = 0
    for lines in ftraincorpus.readlines():
        linesStr = lines.strip("\r\n").split(":::")
        lineclass = linesStr[0]
        content = linesStr[1]
        if(classnums[lineclass] < classtheld):
            fwrite.write(lineclass + ":::" + content)
            fwrite.write("\n")
            classnums[lineclass] = classnums[lineclass] + 1
    for key, val in classnums.items():
        print key, val

if __name__ == "__main__":
    typewords, classlist = headmatch.typewordsDic()
    TrainData(classlist)