# -*- coding:utf-8-*-
from itertools import islice

#处理xml文件
def output(outPath, Path_ConceptsEdges):
    f = open(outPath, 'r')
    fwrite = open(Path_ConceptsEdges, 'w+')
    flag = 0
    elemstr = ""
    lineNums = 3
    for line in islice(f, 3, None):
        lineNums += 1
        #if条件下面用来处理模糊概念
        if(line.find("</concepts>") != -1):
            break
        if(flag == 0):
            conceptID = line.split("\"")[1]
            fwrite.write("n" + conceptID + ": ")
            flag += 1
            continue
        #在没有找到</concept>（整个概念）之前一直输出
        if(line.find("</concept>") == -1):
            elemstr = elemstr + line.strip("\n")
        else:
            elemList = elemstr.split("            </object>")
            objectList = []
            attributeList = []
            attributeValue = []
            for k in range(len(elemList) - 1):
                obj = elemList[k].split("                ")[0].split("\"")[1]
                objectList.append(obj)
            if(elemList[-1] != ''):
                attrList = elemList[-1].split("            </attribute>")
                for m in range(len(attrList) - 1):
                    attr = attrList[m].split("                ")[0].split("\"")[1]
                    attrVal = attrList[m].split("                ")[1].split(">")[1].split("<")[0]
                    attributeList.append(attr)
                    attributeValue.append(attrVal)
            #写入对象
            if(len(objectList) > 1):
                fwrite.write("{")
                for i in range(len(objectList) - 1):
                    fwrite.write(objectList[i] + ",")
                fwrite.write(objectList[-1] + "}")
            if(len(objectList) == 1):
                fwrite.write("{" + objectList[0] + "}")
            if(len(objectList) == 0):
                fwrite.write("{}")
            #写入属性，以及对应的模糊值
            if(len(attributeList) > 1):
                fwrite.write("&" + "{")
                for j in range(len(attributeList) - 1):
                    fwrite.write(attributeList[j] + "/" + attributeValue[j] + ",")
                fwrite.write(attributeList[-1] + "/" + attributeValue[-1] + "}")
            if(len(attributeList) == 1):
                fwrite.write("&" + "{" + attributeList[0] + "/" + attributeValue[0] + "}")
            if(len(attributeList) == 0):
                fwrite.write("&{}")
            fwrite.write("\n")
            flag = 0
            elemstr = ""
    #以下语句用于处理边的链接关系
    f = open(outPath, 'r')
    for line in islice(f, lineNums, None):
        if (line.find("lower_concept_id") != -1):
            lowerEdge = line.split("\"")[1]
            upperEdge = line.split("\"")[3]
            fwrite.write("edges: " + "n" + lowerEdge + "--" + "n" + upperEdge + "\n")




