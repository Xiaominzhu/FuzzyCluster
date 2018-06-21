# -*- coding:utf-8-*-
from __future__ import division

# 计算两个概念之间的相似度(仅仅基于对象)，并写入文件,
# 并返回模糊形式概念字典，如：{'e5':'4,5','e4':'1,2'}
def culSimByQuan(mergePath, simPath):
    fConcepts = open(mergePath, 'r')
    fwrite = open(simPath, 'w+')
    ConceptsDic = {}
    sum = 0
    edgesnum = 0
    for lineCon in fConcepts.readlines():
        lineConList = lineCon.strip("\r\n").split(": ")
        tag = lineConList[0]
        if(tag != "edges"):
            ConceptLabel = tag
            ConceptsList = lineConList[1].split("&")
            ConceptsObj = ConceptsList[0].strip("{").strip("}")
            ConceptsDic[ConceptLabel] = ConceptsObj
        else:
            EdgeList = lineConList[1].split("--")
            Edge1 = EdgeList[0]
            Edge2 = EdgeList[1]
            if(Edge1!='n0' and Edge1 != 'n1' and Edge2 != 'n0' and Edge2 != 'n1'):
                edgesnum += 1
                fobject1 = ConceptsDic[Edge1]                       #模糊概念的对象
                fobject2 = ConceptsDic[Edge2]
                SimValue = Quan(fobject1, fobject2)
                fwrite.write(Edge1 + "--" + Edge2)
                fwrite.write("--" + str(SimValue))
                fwrite.write("\n")
                sum += SimValue
    simThre = sum/edgesnum
    return ConceptsDic, simThre

def Quan(fobject1, fobject2):
    ob1List = fobject1.split(",")
    ob2List = fobject2.split(",")
    sameSum = 0
    disSum = 0
    for elem2 in ob2List:
        ob2 = elem2.split("/")[0]
        val2 = float(elem2.split("/")[1])
        flag = 0
        for elem1 in ob1List:
            ob1 = elem1.split("/")[0]
            val1 = float(elem1.split("/")[1])
            if(ob1 == ob2):
                minval = min([val1, val2])
                maxval = max([val1, val2])
                sameSum += minval
                disSum += maxval
                flag = 1
        if(flag != 1):
            disSum += val2
    return sameSum/disSum

#生成由各个聚类组成的List,如set(['n5', 'n6&n4&n3', 'n2'])
def cluster(simPath, simThre, Nodepath):
    fwrite = open(Nodepath, "w+")
    fsim = open(simPath, 'r')
    edgesSimList = []
    clusterList = []
    clusterGeneration = []
    for line in fsim.readlines():
        linestr = line.strip("\r\n")
        val = linestr.split("--")[2]
        if (float(val) != float(0)):
            edgesSimList.append(linestr)
    j = len(edgesSimList)-1
    nums = 0
    while(j >= 0):
        if(nums % 100 == 0):
            print nums
        nums += 1
        linelist = edgesSimList[j].split("--")
        lower = linelist[0]
        upper = linelist[1]
        value = linelist[2]
        if(float(value) > simThre):
            replacenode = lower + "&" + upper
            replace_update = removesame(replacenode)
            flag = 0
            for k in range(len(edgesSimList) -1):
                lowkey2 = edgesSimList[k].split("--")[0]
                uppkey2 = edgesSimList[k].split("--")[1]
                val2 = edgesSimList[k].split("--")[2]
                if(ifcontain(lowkey2, replace_update)):
                    flag = 1
                    edgesSimList[k] = replace_update + "--" + uppkey2 + "--" + val2
                if(ifcontain(uppkey2, replace_update)):
                    flag = 1
                    edgesSimList[k] = lowkey2 + "--" + replace_update + "--" + val2
            if(flag == 0):
                clusterGeneration.append(replace_update)
            del edgesSimList[j]
        j -= 1
    for elem in edgesSimList:
        clusterList.append(elem.split("--")[0])
        clusterList.append(elem.split("--")[1])
    resultCluster = clusterGeneration + clusterList
    #输出聚类后的节点集合
    for nodeStr1 in set(resultCluster):
        flag_node = 0
        for nodeStr2 in set(resultCluster):
            if(nodeStr1 != nodeStr2):
                if (ifcontain(nodeStr1, nodeStr2)):
                    flag_node = 1
        if (flag_node == 0):
            for node in nodeStr1.split("&"):
                fwrite.write(node + " ")
            fwrite.write("\n")
    return set(resultCluster), edgesSimList

#判断str11是否在str2中，如 n21&n23 在 n21&n22&n23
def ifcontain(str1,str2):
    str1Set= set(str1.split("&"))
    str2Set = set(str2.split("&"))
    if(str1Set.intersection(str2Set) == str1Set):
        return True
    return False

def removesame(replacenode):
    nodeList = replacenode.split("&")
    node_update = list(set(nodeList))
    updateStr = node_update[0]
    node_set = set(node_update[1:])
    for edge in node_set:
        updateStr = updateStr + "&" + edge
    return updateStr

#利用对象表示出来
def clusterResult(clusterSet, ConceptsDic):
    clusterGroup = []
    for elemstr in clusterSet:
        clustertmp = []
        nodeList = elemstr.split("&")
        for elem in nodeList:
            objlist = ConceptsDic[elem].split(",")
            for objVal in objlist:
                clustertmp.append(objVal.split("/")[0])
        if(list(set(clustertmp)) not in clusterGroup):
            clusterGroup.append(list(set(clustertmp)))
    return clusterGroup

#聚类组的过滤
def filterSameCluster(clusterGroup, IDpath):
    fwrite = open(IDpath, 'w+')
    updateclusterGroup = []
    for i in range(len(clusterGroup)):
        flag = 0
        for j in range(len(clusterGroup)):
            tmpSet = set(clusterGroup[i]).intersection(clusterGroup[j])
            # if ((i != j and tmpSet == set(clusterGroup[i]))
            #      or (i != j and len(tmpSet) >= len(set(clusterGroup[i]))*1/2)):
            if (i != j and tmpSet == set(clusterGroup[i])):
                flag += 1
                break
        if(flag == 0):
            updateclusterGroup.append(clusterGroup[i])
    k = 0
    for lineelem in updateclusterGroup:
        k += 1
        for i in lineelem:
            fwrite.write(i + ",")
        fwrite.write("\n")
    return updateclusterGroup








