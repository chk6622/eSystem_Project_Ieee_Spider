#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 28, 2018

@author: xingtong
'''
from threading import Thread
from logger.LogConfig import appLogger
from utiles.PrintTool import PrintTool
from Queue import Queue
import threading


ser1Lock = threading.Lock()

class NormalThread(threading.Thread):
#     taskQueue=None
#     apiSpider=None
#     webPageSpider=None
#     mongoDBDAO=None
#     printTool=None
    
    
    def __init__(self,taskQueue,apiSpider,webPageSpider,mongoDBDAO,printTool):
        threading.Thread.__init__(self)
        self.taskQueue=taskQueue
        self.apiSpider=apiSpider
        self.webPageSpider=webPageSpider
        self.mongoDBDAO=mongoDBDAO
        self.printTool=printTool
        
    def run(self):
        appLogger.info('Thread %s start' % self.getName())
        if not self.taskQueue:
            return
        while True:
            try:
                ser1Lock.acquire()
                if self.taskQueue.empty():
                    ser1Lock.release()
                    break
                result=self.taskQueue.get(block=True)
                ser1Lock.release()
                
                self.printTool.printStartMessage('%s - processes result' %threading.Thread.getName(self))
                self.printTool.printStartMessage('%s - gets pdf url' %threading.Thread.getName(self))
                pdfUrl=self.apiSpider.getPdfUrl(result)
        #             print pdfUrl
                pdfRealUrl=self.webPageSpider.getRealPdfUrl(pdfUrl)
        #             print pdfRealUrl
                self.printTool.printEndMessage('%s - gets pdf url' %threading.Thread.getName(self))
                self.printTool.printStartMessage('%s - gets pdf file' %threading.Thread.getName(self))
                if pdfRealUrl:            #if real file not exist then use simulated file
                    fileName=result.get('article_number')+'.pdf'
                else:
                    fileName='simulated file.pdf'
                fileTempPath=self.webPageSpider.generateTempFilePath(fileName)
                fileId=''
                flag=self.webPageSpider.getPdfFile(pdfRealUrl, fileTempPath)
                self.printTool.printEndMessage('%s - gets pdf file' %threading.Thread.getName(self))
                self.printTool.printStartMessage('%s - inserts pdf file into the database' %threading.Thread.getName(self))
                if flag:  #if get pdf file success then save the file into the database
                    fileId=self.mongoDBDAO.insertFile(fileTempPath, fileName, isDelFile=True)
                else:
                    fileId=self.mongoDBDAO.insertFile(fileTempPath, fileName, isDelFile=False)
                self.printTool.printEndMessage('%s - inserts pdf file into the database' %threading.Thread.getName(self))
                self.printTool.printStartMessage('%s - inserts articles into the database' %threading.Thread.getName(self))
                result['fileId']=fileId  #set fileId in the result
                self.mongoDBDAO.insertOneData(**result)  #save a result into the database
                self.printTool.printEndMessage('%s - inserts articles into the database' %threading.Thread.getName(self))
                self.printTool.printEndMessage('%s - processes result' %threading.Thread.getName(self))
            except Exception,err:
                appLogger.error(err)
            finally:
                try:
                    ser1Lock.release()
                except Exception, err:
                    pass
        appLogger.info('Thread %s end' % self.getName())
    

if __name__ == '__main__':
    pass