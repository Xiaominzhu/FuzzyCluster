# -*- coding:utf-8-*-

#处理xml文件
def mergeoutput(nodepath, nodepath_Tr, fmergePath):
    f = open(nodepath,'r')
    fTr = open(nodepath_Tr, 'r')
    fwrite = open(fmergePath, 'w+')
    conceptTr = []
    for lineTr in fTr.readlines():
        lineTrList = lineTr.strip('\r\n').split(": ")
        nodeTrlabel = lineTrList[0]
        if(nodeTrlabel != "edges"):
            objTrList = lineTrList[1].split("&")[1].strip("{").strip("}").split(",")
            if(objTrList[0] != ''):
                conceptTr.append(objTrList)
    for line in f.readlines():
        lineList = line.strip('\r\n').split(": ")
        nodelabel = lineList[0]
        if(nodelabel != "edges"):
            objstrList = lineList[1].split("&")[0].strip("{").strip("}").split(",")
            for objTrlist in conceptTr:
                tmp = match(objTrlist, objstrList)
                if(tmp != "0"):
                    fwrite.write(nodelabel+ ": ")
                    fwrite.write("{" + tmp + "}&")
                    fwrite.write(lineList[1].split("&")[1])
                    fwrite.write("\n")
        else:
            fwrite.write(line)

def match(objTrlist, objstrList):
    elemTrdic = {}
    objTrList = []
    for objVal in objTrlist:
        objTr = objVal.split("/")[0]
        val = objVal.split("/")[1]
        objTrList.append(objTr)
        elemTrdic[objTr] = val
    if(set(objstrList) == set(objTrList)):
        writeStr = ""
        for i in range(len(objstrList) - 1):
            writeStr += objstrList[i] + "/" + elemTrdic[objstrList[i]] + ","
        writeStr += objstrList[-1] + "/" + elemTrdic[objstrList[-1]]
        return writeStr
    else:
        return "0"