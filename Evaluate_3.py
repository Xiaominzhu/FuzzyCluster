# -*- coding:utf-8-*-
from __future__ import division
from collections import Counter
import thread
import time
from pylab import *
import matplotlib.pyplot as plt
import numpy
from function import clusterByQuan, clusterByZxm

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 返回字典，key:节点， value: 对象||属性
def nodeDic(mergePath):
    fread = open(mergePath, 'r')
    nodedic = {}
    for line in fread.readlines():
        lineList = line.strip("\r\n").split(": ")
        node = lineList[0]
        if (node != "edges"):
            concept = lineList[1]
            objvalueList = concept.split("&")[0].strip("{").strip("}").split(",")
            attvalueList = concept.split("&")[1].strip("{").strip("}").split(",")
            objList = []
            attrList = []
            for obj in objvalueList:
                objList.append(obj.split("/")[0])
            for attr in attvalueList:
                attrList.append(attr.split("/")[0])
            nodedic[node] = ",".join(objList) + "||" + ",".join(attrList)
    return nodedic

# 计算对象，属性，隶属度字典
def objectValDic(fPathNor):
    fread = open(fPathNor, 'r')
    objectValdic = {}
    news = 0
    for line in fread.readlines():
        lineStr = line.strip(",\r\n")
        for attrvalue in lineStr.split(","):
            attr = attrvalue.split(":")[0]
            value = attrvalue.split(":")[1]
            objectValdic[str(news) + "&" + attr] = value
        news += 1
    return objectValdic

# 计算平均聚类质量
def inclass(path, nodedic, objectValdic):
    fread = open(path, "r")
    sumerrorList = []
    nums = 0
    for line in fread.readlines():
        nums += 1
        # print nums
        thread.start_new_thread(threadBody, (line, sumerrorList, nodedic, objectValdic))
        if nums % 10 == 0:
            time.sleep(1)
    return 1 - sum(sumerrorList) / len(sumerrorList)

#多线程实现
def threadBody(line, sumerrorList, nodedic, objectValdic):
    sumerror = 0
    lineStr = line.strip(" \r\n")
    nodeList = lineStr.split(" ")
    objectList = []
    attributeList = []
    for node in nodeList:
        objtmp = nodedic[node].split("||")[0].split(",")     # 获取该簇中所有出现的对象
        attrtmp = nodedic[node].split("||")[1].split(",")    # 获取该簇中所有出现的属性
        objectList.extend(objtmp)
        attributeList.extend(attrtmp)
    wordcount = Counter(objectList)
    objectSetList = list(set(objectList))
    objLen = len(objectSetList)
    for attrelem in set(attributeList):
        for i in range(objLen):
            for j in range(objLen):
                if (i != j):
                    obj1 = objectSetList[i]
                    obj2 = objectSetList[j]
                    dis_obj1 = objectValdic.get(obj1 + "&" + attrelem, 0)
                    dis_obj2 = objectValdic.get(obj2 + "&" + attrelem, 0)
                    dis = abs(float(dis_obj1) - float(dis_obj2))
                    if (dis > 0):
                        p_obj1 = wordcount[obj1] / len(nodeList)
                        p_obj2 = wordcount[obj2] / len(nodeList)
                        sumerror += p_obj1 * p_obj2 * dis
                    else:
                        sumerror = 0
    sumerrorList.append(sumerror)

# Quan等提出方法的平均聚类质量
def evaluate_Quan():
    path = 'F:/englishPaper/evaluateFeatures/'
    quanList = []
    for featureNums in range(9, 16):
        mergePath = path + "ConceptsEdgesMerge_" + str(featureNums) + ".txt"
        simPath = path + "SimByQuan_" + str(featureNums) + ".txt"
        ConceptsDic, simThre = clusterByQuan.culSimByQuan(mergePath, simPath)
        Nodepath = path + "ByNode_Quan_" + str(featureNums) + ".txt"
        clusterByZxm.cluster(simPath, simThre, Nodepath)

        fPathNor = path + "JieBaNor_" + str(featureNums) + ".txt"
        nodedic = nodeDic(mergePath)
        objectValdic = objectValDic(fPathNor)
        averSimQuan = inclass(Nodepath, nodedic, objectValdic)
        quanList.append(averSimQuan)
    return quanList

# 本文提出方法的平均聚类质量
def evaluate_zxm():
    path = 'F:/englishPaper/evaluateFeatures/'
    zxmList = []
    for featureNums in range(9, 16):
        for afa in numpy.arange(0.1, 1, 0.1):
            bta = 1 - afa
            mergePath = path + "ConceptsEdgesMerge_" + str(featureNums) + ".txt"
            simPath = path + "SimByZxm_" + str(featureNums) + ".txt"
            ConceptsDic, simThre = clusterByZxm.culSimByZxm(afa, bta, mergePath, simPath)
            Nodepath = path + "ByNode_zxm_" + str(featureNums) + ".txt"
            clusterByZxm.cluster(simPath, simThre, Nodepath)

            fPathNor = path + "JieBaNor_" + str(featureNums) + ".txt"
            nodedic = nodeDic(mergePath)
            objectValdic = objectValDic(fPathNor)
            averSimzxm = inclass(Nodepath, nodedic, objectValdic)
            zxmList.append(averSimzxm)
    return zxmList

def figure(quanList, zxmList):
    x = []
    for i in range(10, 15):
        x.append(i)
    plt.plot(x, zxmList, linewidth=3, color='r', marker='s',
             markerfacecolor='r', markersize=10, linestyle="-", label= "本文方法")
    plt.plot(x, quanList, linewidth=3, color='g', marker='s',
             markerfacecolor='g', markersize=10, linestyle="-", label= "方法")
    myfont = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/Arial.ttf')  # 获取字体
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    plt.title('聚类质量', fontsize=18)
    plt.xlabel('特征词个数', fontsize=18)
    plt.ylabel('聚类质量', fontsize=18)
    plt.legend(loc='upper left')
    plt.ylim(0.5, 1, 0.1)        # 设置坐标轴
    plt.xlim(10, 15, 1)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.show()

if __name__ == '__main__':
    quanList = evaluate_Quan()
    zxmList = evaluate_zxm()
    figure(quanList, zxmList)





