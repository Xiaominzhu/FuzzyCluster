# -*- coding:utf-8-*-
from __future__ import division
from function import processOutput, merge

def Output():
    path = 'F:/englishPaper/evaluateFeatures/'
    for featureNums in range(9, 16):
        outPath = path + "Output_" + str(featureNums) + ".xml"
        ConEdgPath = path + "ConceptsEdges_" + str(featureNums) + ".txt"
        processOutput.output(outPath, ConEdgPath)

        outPath_Tr = path + "Output_Tr_" + str(featureNums) + ".xml"
        ConEdgPath_Tr = path + "ConceptsEdges_Tr_" + str(featureNums) + ".txt"
        processOutput.output(outPath_Tr, ConEdgPath_Tr)

        fmergePath = path + "ConceptsEdgesMerge_" + str(featureNums) + ".txt"
        merge.mergeoutput(ConEdgPath, ConEdgPath_Tr, fmergePath)

if __name__ == '__main__':
    Output()
