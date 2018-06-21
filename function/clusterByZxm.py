# -*- coding:utf-8-*-
from __future__ import division

#计算两个概念之间的相似度，并写入文件,
# 并返回模糊概念字典，如：{'e5':'4,5||b/0.7','e4':'1,2||a/0.7,c/0.6}
def culSimByZxm(afa, bta, path, fPath):
    fConcepts = open(path, 'r')
    fwrite = open(fPath, 'w+')
    ConceptsDic = {}
    sum = 0
    edgesnum = 0
    for lineCon in fConcepts.readlines():
        lineConList = lineCon.strip("\r\n").split(": ")
        tage = lineConList[0]
        if(tage != "edges"):
            ConceptLabel = lineConList[0]
            ConceptsList = lineConList[1].split("&")
            ConceptsOb = ConceptsList[0].strip("{").strip("}")
            ConceptsAtt = ConceptsList[1].strip("{").strip("}")
            ConceptsDic[ConceptLabel] = ConceptsOb + "||" + ConceptsAtt
        else:
            EdgeList = lineConList[1].split("--")
            Edge1 = EdgeList[0]
            Edge2 = EdgeList[1]
            if (Edge1 != 'n0' and Edge1 != 'n1' and Edge2 != 'n0' and Edge2 != 'n1'):
                edgesnum += 1
                Concepts1 = ConceptsDic[Edge1]
                Concepts2 = ConceptsDic[Edge2]
                SimValue = Quan_update(Concepts1, Concepts2, afa, bta)
                fwrite.write(Edge1 + "--" + Edge2)
                fwrite.write("--" + str(SimValue))
                fwrite.write("\n")
                sum += SimValue
    simThre = sum/edgesnum
    return ConceptsDic, simThre

def Quan_update(Concepts1, Concepts2, afa, bta):
    fobject1 = Concepts1.split("||")[0]
    fobject2 = Concepts2.split("||")[0]
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
        if(flag == 0):
            disSum += val2
    objectSim = afa*sameSum/disSum

    #计算属性相似度
    fattr1 = Concepts1.split("||")[1]
    fattr2 = Concepts2.split("||")[1]
    attr1List = fattr1.split(",")
    attr2List = fattr2.split(",")
    sameSum_attr = 0
    disSum_attr = 0
    for elem1_attr in attr1List:
        attr1 = elem1_attr.split("/")[0]
        val1_attr = float(elem1_attr.split("/")[1])
        flag_attr = 0
        for elem2_attr in attr2List:
            attr2 = elem2_attr.split("/")[0]
            val2_attr = float(elem2_attr.split("/")[1])
            if(attr1 == attr2):
                minval_attr = min([val1_attr, val2_attr])
                maxval_attr = max([val1_attr, val2_attr])
                sameSum_attr += minval_attr
                disSum_attr += maxval_attr
                flag_attr = 1
        if(flag_attr == 0):
            disSum_attr += val1_attr
    attributeSim = bta*sameSum_attr/disSum_attr
    return objectSim + attributeSim

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

# 生成由各个聚类组成的List,如set(['n5', 'n6&n4&n3', 'n2'])
def cluster(simPath, simThre, Nodepath):
    fwrite = open(Nodepath, "w+")
    fsim = open(simPath, 'r')
    edgesSimList = []
    clusterList = []
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
        replacenode = lower + "&" + upper
        replace_update = removesame(replacenode)
        value = linelist[2]
        if(float(value) >= simThre):
            del edgesSimList[j]
            for k in range(len(edgesSimList)):
                lowkey2 = edgesSimList[k].split("--")[0]
                uppkey2 = edgesSimList[k].split("--")[1]
                val2 = edgesSimList[k].split("--")[2]
                if(ifcontain(lowkey2, upper)):
                    edgesSimList[k] = replace_update + "--" + uppkey2 + "--" + val2
                if(ifcontain(uppkey2, upper)):
                    edgesSimList[k] = lowkey2 + "--" + replace_update + "--" + val2
        j -= 1
    for elem in edgesSimList:
        clusterList.append(elem.split("--")[0])
        clusterList.append(elem.split("--")[1])

    # 删除被包含的聚类
    for nodeStr1 in set(clusterList):
        flag_node = 0
        for nodeStr2 in set(clusterList):
            if(nodeStr1 != nodeStr2):
                if (ifcontain(nodeStr1, nodeStr2)):
                    flag_node = 1
        if (flag_node == 0):
            for node in nodeStr1.split("&"):
                fwrite.write(node + " ")
            fwrite.write("\n")
    return set(clusterList), edgesSimList

def clusterResult(clusterSet, ConceptsDic):
    clusterGroup = []
    for elemstr in clusterSet:
        clustertmp = []
        nodeList = elemstr.split("&")
        for elem in nodeList:
            objlist = ConceptsDic[elem].split("||")[0].split(",")
            for objVal in objlist:
                clustertmp.append(objVal.split("/")[0])
        if(list(set(clustertmp)) not in clusterGroup):
            clusterGroup.append(list(set(clustertmp)))
    return clusterGroup

# 聚类组的过滤
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
    return k
