# -*- coding:utf-8-*-
import jieba
from clusterByzxm import newcluster_4
jieba.load_userdict("F:/graduationThesis/dataSet/test/addDict.txt")
usenature = ("Ag","an","b","dg","g","h","i",
          "j","k","l","Ng","n","nr","ns","nt","nz",
          "s","tg","t","vg","vd","vn","x","z",
          "un")

def level(edgesSimList, levelPath):
    fwrite = open(levelPath, 'w+')
    edgesDic = {}
    for noderelation in edgesSimList:
        lower = noderelation.split("--")[0]
        upper = noderelation.split("--")[1]
        if(upper not in edgesDic.keys()):
            edgesDic[upper] = []
        if (upper in edgesDic.keys()):
            edgesDic[upper].append(lower)
    lasttmp = []
    for key, items in edgesDic.items():
        for elem in key.split("&"):
            fwrite.write(elem + " ")
        fwrite.write("\n")
        for val in items:
            listtmp = [ele for ele in val.split("&")]
            if(set(listtmp).intersection(lasttmp) != set(listtmp)):
                for el in listtmp:
                    fwrite.write(el + " ")
                fwrite.write("\n")
            lasttmp = listtmp
        fwrite.write("************************" + "\n")
    return edgesDic

def conceptsDic():
    conpath = "F:/graduationThesis/dataSet/test/clusterTask/ConceptsEdges_merge.txt"
    fConcepts = open(conpath, 'r')
    conceptsdic = {}
    for lineCon in fConcepts.readlines():
        lineConList = lineCon.strip("\r\n").split(": ")
        tag = lineConList[0]
        if (tag != "edges"):
            ConceptLabel = tag
            ConceptsList = lineConList[1].split("&")
            ConceptsAttr = ConceptsList[1].strip("{").strip("}")
            conceptsdic[ConceptLabel] = ConceptsAttr
    return conceptsdic

def getwords(levelPath, conceptsdic, wordsPath):
    fnode = open(levelPath, 'r')
    fwrite = open(wordsPath, 'w+')
    for line in fnode.readlines():
        if(line.strip("\r\n") == "************************"):
            fwrite.write(line)
        else:
            words_tmp = []
            lineList = line.strip(" \r\n").split(" ")
            for node in lineList:
                for wdval in conceptsdic[node].split(","):
                    words_tmp.append(wdval.split("/")[0])
            for wor in set(words_tmp):
                fwrite.write(wor + " ")
            fwrite.write("\n")
            fwrite.flush()

if __name__ == '__main__':
    mergePath = "F:/graduationThesis/dataSet/test/clusterTask/ConceptsEdges_merge.txt"
    simPath = 'F:/graduationThesis/dataSet/test/clusterTask/SimByAll.txt'
    afa = 0.5
    bta = 0.5
    ConceptsDic, simThre = newcluster_4.culSim(afa, bta, mergePath, simPath)
    simThre1 = 0.3
    Nodepath = "F:/graduationThesis/dataSet/test/clusterTask/ByNode_zxm.txt"
    clusterSet, edgesSimList = newcluster_4.cluster(simPath, simThre1, Nodepath)

    levelPath = "F:/graduationThesis/dataSet/test/clusterTask/level_node.txt"
    level(edgesSimList, levelPath)
    wordsPath = "F:/graduationThesis/dataSet/test/clusterTask/level_words.txt"
    conceptsdic = conceptsDic()
    getwords(levelPath, conceptsdic, wordsPath)