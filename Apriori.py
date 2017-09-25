"""
Created by yfDong on 9/25/17.
"""
# coding=utf-8
from numpy import *

def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(dataset):                  #生成元素个数为1的项集
    C1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))

def scanD(D, Ck, minSupport):      #生成k项频繁项集和其支持度
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                ssCnt[can] = ssCnt.get(can, 0)+1
    numItem = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItem
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k):                #生成k项候选集
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet, minSupport = 0.5 ):  #迭代生成所有频繁项集及其支持度
    C1 = createC1(dataSet)
    #D = dataSet
    D = list(map(set, dataSet))
    L1, supportData = scanD(D, C1, minSupport)
    L= [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2],k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

"""    频繁项集测试数据
dataSet = loadDataSet()
print(dataSet)
C1 = createC1(dataSet)
print(C1)
D = list(map(set, dataSet))
print(D)
L1, suppDat = scanD(D, C1, 0.5)
print(L1)
L, suppDat = apriori(dataSet)
print(L)
"""
#关联规则
def generateRules(L, suportData, minConf = 0.7):     #关联规则生成函数
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if(i > 1):
                #三个及以上元素的集合
                H1 = calConf(freqSet, H1, suportData, bigRuleList, minConf)
                rulesFromConseq(freqSet, H1, suportData, bigRuleList, minConf)
            else:
                #两个元素的集合
                calConf(freqSet, H1, suportData, bigRuleList, minConf)
    return bigRuleList

def calConf(freqSet, H, supportData, brl, minConf = 0.7):
    prundH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print(freqSet - conseq, '-->',conseq, 'conf :', conf)
            brl.append((freqSet - conseq, conseq, conf))
            prundH.append(conseq)
    return prundH

def rulesFromConseq(freqSet, H, supportData, brl, minConf = 0.7):
    m = len(H[0])
    if len(freqSet) > (m + 1):
        Hmpl = aprioriGen(H, m+1)
        Hmpl = calConf(freqSet, Hmpl, supportData, brl, minConf)
        if len(Hmpl) > 1:
            rulesFromConseq(freqSet, Hmpl, supportData, brl, minConf)

"""    关联规则测试
dataSet = loadDataSet()
L, suppData = apriori(dataSet, minSupport=0.5)
rules = generateRules(L, suppData, minConf=0.7)
"""

"""    提高Apriori算法效率
1.基于散列的技术
2.事务压缩
3.划分
4.抽样
5.动态项集计数
"""
