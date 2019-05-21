#!/usr/bin/env python
#coding: utf-8
'''
Created on Sep 19, 2018

@author: xingtong
'''

import math


def GrieFunc(vardim, x, bound):
    """
    Griewangk function
    """
    s1 = 0.
    s2 = 1.
    for i in range(1, vardim + 1):
        s1 = s1 + x[i - 1] ** 2
        s2 = s2 * math.cos(x[i - 1] / math.sqrt(i))
    y = (1. / 4000.) * s1 - s2 + 1
    y = 1. / (1. + y)
    return y


def RastFunc(vardim, x, bound):
    """
    Rastrigin function
    """
    s = 10 * 25
    for i in range(1, vardim + 1):
        s = s + x[i - 1] ** 2 - 10 * math.cos(2 * math.pi * x[i - 1])
    return s

def getPipelineFuncFitness(varDim, varValues):
    '''
    Get the pipeline function fitness
    @param varDim: the number of variables
    @param varValues: the value of every variables
    @return: the pipeline function fitness
    '''
    max=0
    timeArray=[]
    timeArray.append(getPdfUrlTime)
    timeArray.append(getPdfFileTime)
    timeArray.append(insertPdfFileTime)
    timeArray.append(insertArticleTime)
    for i in range(1, varDim+1):
        tmp1=timeArray[i-1](varValues[i-1])
        tmp2=tmp1/varValues[i-1]
        if tmp2>max:
            max=tmp2
    return 1/max

def getPdfUrlTime(nt):
    '''
    @param nt:the number of thread processing this stage
    @return: average time to process every data 
    '''
    dReturn=0
    if nt>0:
        dReturn=0.0076*nt+1.4877
    return dReturn

def getPdfFileTime(nt):
    '''
    @param nt:the number of thread processing this stage
    @return: average time to process every data 
    '''
    dReturn=0
    if nt>0:
        dReturn=0.0008*(nt**3)-0.0169*(nt**2)+0.6207*nt+11.244
    return dReturn

def insertPdfFileTime(nt):
    '''
    @param nt:the number of thread processing this stage
    @return: average time to process every data 
    '''
    dReturn=0
    if nt>0:
        dReturn=0.0014*nt+0.38
    return dReturn

def insertArticleTime(nt):
    '''
    @param nt:the number of thread processing this stage
    @return: average time to process every data 
    '''
    dReturn=0
    if nt>0:
        dReturn=0.0014*nt+0.1911
    return dReturn

if __name__=='__main__':
    nt=50
#     print getPdfUrlTime(nt)
#     print getPdfFileTime(nt)
#     print insertPdfFileTime(nt)
#     print insertArticleTime(nt)
#     print 0.4941*(50**3)
#     print 5.2656*(50**2)
#     print 18.901*50
#     print 0.4941*(50**3)-5.2656*(50**2)+18.901*50-4.1819
    
    v=4
    x=[49,         23.39850626, 21,         10,        ]
    print PipelineFunc(v, x)
    x=[91,         23.39838123,  1,          2        ]
    print PipelineFunc(v, x)
    x=[20,         23.39849636, 23,         21        ]
    print PipelineFunc(v, x)
    
    
    
    
    
    
    
    
    
    