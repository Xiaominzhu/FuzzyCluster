# -*- coding:utf-8-*-
from __future__ import division
from function import preproccess_1, preprocess_2

# 不同数据集
def extractFFc():
    path = 'F:/englishPaper/evaluateFeatures/'
    for featureNums in range(13, 16):
        print "featureNums: ", featureNums
        fPath = path + "JieBa_" + str(featureNums) + ".txt"
        preproccess_1.jiebaSe(featureNums, fPath)
        fPathNor = path + "JieBaNor_" + str(featureNums) + ".txt"
        preproccess_1.normalization(fPath, fPathNor)
        fPathNorInput = path + "sportsInput_" + str(featureNums) + ".txt"
        preproccess_1.getInput(fPathNor, fPathNorInput)

        #计算转置情况
        fPathNor_Tr = path + "JieBaNor_Tr_" + str(featureNums) + ".txt"
        preprocess_2.contextTr(fPathNor, fPathNor_Tr)
        fPathNor_Tr_Input = path + "sportsInput_Tr_" + str(featureNums) + ".txt"
        preprocess_2.getInput_Tr(fPathNor_Tr, fPathNor_Tr_Input)

if __name__ == '__main__':
    extractFFc()
