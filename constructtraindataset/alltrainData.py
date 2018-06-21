# -*- coding:utf-8-*-
from __future__ import division
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def alltrain():
    rootpath = "F:/graduationThesis/dataSet/test/classifiByThreeConcepts/"
    path = rootpath + "traindata3/"
    fwrite = open(rootpath + "traindata.txt", 'w+')
    namelist = os.listdir(path)
    for n in namelist:
        print n
        for line in open(path + n).readlines():
            fwrite.write(line)
if __name__ == '__main__':
    alltrain()
