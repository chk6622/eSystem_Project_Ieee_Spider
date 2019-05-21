#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 28, 2018

@author: xingtong
'''

from ieeexplorespider.ApiSpider import IeeeApiSpider
from ieeexplorespider.TestWebPageSpider import WebPageSpider
from dao.MongoDBDAO import MongoDBDAO
from utiles.PrintTool import PrintTool
from ConfigParser import ConfigParser
from logger.LogConfig import appLogger
from Queue import Queue
from normalthread.NormalThread import NormalThread
import threading
import thread
import time

def getDatabase(appConfig):
    dbName=appConfig.get('DB', 'DB_NAME')
    dbHost=appConfig.get('DB', 'DB_HOST')
    dbPort=appConfig.get('DB', 'DB_PORT')
    dbUser=appConfig.get('DB', 'DB_USER')
    dbPass=appConfig.get('DB', 'DB_PASS')
    dbColl=appConfig.get('DB', 'DB_COLL')
    dbBinColl=appConfig.get('DB', 'DB_COLL_BIN')
    return MongoDBDAO(dbName,dbHost,dbPort,dbUser,dbPass,dbColl,dbBinColl)

def getWebPageSipder(appConfig):
    mainPageUrl=appConfig.get('WebPageSpider','MAIN_PAGE_URL')
    cookiePath=appConfig.get('WebPageSpider','COOKIE_PATH')
    tempDocPath=appConfig.get('WebPageSpider','TEMP_DOC_PATH')
    return WebPageSpider(mainPageUrl,cookiePath,tempDocPath)

def getApiSpider(appConfig):
    apiKey=appConfig.get('ApiSpider','API_KEY')
    queryReturnMaxResult=appConfig.getint('ApiSpider','QUERY_RETURN_MAX_RESULTS')
    maxQueryCountLimit=appConfig.getint('ApiSpider','MAX_QUERY_COUNT_LIMIT')
    queryBeginYear=appConfig.get('ApiSpider','QUERY_BEGIN_YEAR')
    queryEndYear=appConfig.get('ApiSpider','QUERY_END_YEAR')
    return IeeeApiSpider(apiKey,queryReturnMaxResult,maxQueryCountLimit,queryBeginYear,queryEndYear)

def getKeywords(appConfig):
    aReturn=None
    keyWords=appConfig.get('KayWords','KEY_WORDS')
    if keyWords:
        aReturn=keyWords.split(',')
    return aReturn

def getTHreadCount(appConfig):
    tReturn=1
    try:
        tReturn=appConfig.getint('NormalMultithreading','THREAD_COUNT')
    except Exception, err:
        print err
    return tReturn

def isThreadAlive(threadArray):
    '''
    if any thread in the threadArray is alive
    @param threadArray: a array which contains thread obj
    @return: if any thread in the threadArray is alive than return true,or return false
    '''
    bReturn=False
    if threadArray:
        for t in threadArray:
            if t.isAlive():
                bReturn=True
                break
    return bReturn


    

if __name__ == '__main__':
    pt=PrintTool()
    pt.printStartMessage('Ieee xplore spider')
    #initialize app
    configFilePath='../config.conf'
    cf = ConfigParser()
    cf.read(configFilePath)
    keyWords=getKeywords(cf)
    
    pt.printStartMessage('initiate')
    apiSpider=getApiSpider(cf)
    webPageSpider=getWebPageSipder(cf)
    mongoDBDAO=getDatabase(cf)
    threadCount=getTHreadCount(cf)
    
    #
    pt.printEndMessage('initiate')
    pt.printStartMessage('processes')
    taskQueue=Queue()  
    for keyWord in keyWords:
        appLogger.info('------------------------------------------------------------')
        pt.printStartMessage('query articles by keywords:'+keyWord)
        results=apiSpider.queryData(keyWord)
        pt.printEndMessage('query articles by keywords:'+keyWord)
        if not results or len(results)==0:
            print 'Results number is 0'
            break
        else:
            print 'Results number is %d' % len(results)
            for result in results:
                taskQueue.put(result)
        
        pt.printStartMessage('processes result set')
        threadArray=[]
        for i in range(threadCount):
            nt=NormalThread(taskQueue,apiSpider,webPageSpider,mongoDBDAO,pt)
            threadArray.append(nt)
            nt.start()
        while True:
            if isThreadAlive(threadArray):
                time.sleep(1)
            else:
                break
        pt.printEndMessage('processes result set')
    pt.printEndMessage('Ieee xplore spider')
    pt.getTotalStatistics()        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        