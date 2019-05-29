#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 26, 2018

@author: xingtong
'''
from ieeexplorespider.ApiSpider import IeeeApiSpider
from ieeexplorespider.TestWebPageSpider import WebPageSpider
from dao.MongoDBDAO import MongoDBDAO
from utiles.PrintTool import PrintTool
from ConfigParser import ConfigParser
from logger.LogConfig import appLogger

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

if __name__ == '__main__':
    pt=PrintTool()
    pt.printStartMessage('Ieee xplore spider')
    #initialize app
    configFilePath='../config.conf'
    cf = ConfigParser()
    cf.read(configFilePath)
    keyWords=getKeywords(cf)
    
    pt.printStartMessage('Initializing')
    apiSpider=getApiSpider(cf)
    webPageSpider=getWebPageSipder(cf)
    mongoDBDAO=getDatabase(cf)
    
    #
    pt.printEndMessage('Initializing')
#     pt.printStartMessage('processing')
    for keyWord in keyWords:
#         appLogger.info('------------------------------------------------------------')
        pt.printStartMessage('Key word: %s' % keyWord)
        results=apiSpider.queryData(keyWord)
#         pt.printEndMessage('query articles by keywords:'+keyWord)
        if not results or len(results)==0:
            print 'Results number is 0'
            break
#         else:
#             print 'Results number is %d' % len(results)
#         pt.printStartMessage('processes result set')
        pt.printStartMessage('Crawling %d articles' % len(results))
        resultNum=0
        for (ind,result) in enumerate(results):
#             appLogger.info('----------------------------%d--------------------------------' % resultNum)
            resultNum+=1
            pt.printStartMessage('Crawling the %dth article:' % (ind+1))
#             pt.printStartMessage('gets pdf url')
            pdfUrl=apiSpider.getPdfUrl(result)
            pdfRealUrl=webPageSpider.getRealPdfUrl(pdfUrl)
#             pt.printEndMessage('gets pdf url')
#             pt.printStartMessage('gets pdf file')
            if pdfRealUrl:            #if real file not exist then use simulated file
                fileName=result.get('article_number')+'.pdf'
            else:
                fileName='simulated file.pdf'
            fileTempPath=webPageSpider.generateTempFilePath(fileName)
            fileId=''
            flag=webPageSpider.getPdfFile(pdfRealUrl, fileTempPath)
#             pt.printEndMessage('gets pdf file')
#             pt.printStartMessage('inserts pdf file into the database')
            if flag:  #if get pdf file success then save the file into the database
                fileId=mongoDBDAO.insertFile(fileTempPath, fileName, isDelFile=True)
            else:
                fileId=mongoDBDAO.insertFile(fileTempPath, fileName, isDelFile=False)
#             pt.printEndMessage('inserts pdf file into the database')
#             pt.printStartMessage('inserts articles into the database')
            result['fileId']=fileId  #set fileId in the result
            mongoDBDAO.insertOneData(**result)  #save a result into the database
#             pt.printEndMessage('inserts articles into the database')
            pt.printEndMessage('Crawling the %dth article:' % (ind+1))
#             appLogger.info('----------------------------%d--------------------------------' % resultNum)
#         pt.printEndMessage('processes result set')
        pt.printEndMessage('Crawling %d articles' % len(results))
#         appLogger.info('-------------------------------------------------------------')
#     pt.printEndMessage('processing')
    pt.printEndMessage('Ieee xplore spider')
    