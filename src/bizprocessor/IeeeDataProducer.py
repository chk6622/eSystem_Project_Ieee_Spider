#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 30, 2018

@author: xingtong
'''

from baseprocessor.BaseProcessor import BaseProcessor
from ieeexplorespider.ApiSpider import IeeeApiSpider
from model.StreamBox import StreamBox
from model.StopSignal import StopSignal
from logger.LogConfig import appLogger
from logger.StreamLogger import StreamLogger
import time

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

class IeeeDataProducer(BaseProcessor):
    '''
    this class produces data which needs to be processed by streamline
    '''
    productCount=0
    
    def __init__(self,inputQueue=None,outputQueue=None):
        super(IeeeDataProducer,self).__init__(inputQueue=inputQueue,outputQueue=outputQueue)
        self.apiSpider=getApiSpider(self.appConfig)
        self.generater=self.getResultData()
            
    def process(self,processObj=None):
        try:
            streamBox=StreamBox()
            streamBox.result=self.generater.next()
            return streamBox
        except StopIteration:
            return StopSignal()
        except Exception,e:
            appLogger.error(e)
            return None
        
    def getResultData(self):
        keyWords=getKeywords(self.appConfig)
        for keyWord in keyWords:
            results=self.apiSpider.queryData(keyWord)
            if not results or len(results)==0:
                appLogger.info('key word: %s results number is 0' % keyWord)
            else:
                appLogger.info('key word: %s results number is %d' % (keyWord,len(results)))
                for result in results:
                    yield result
            
        
    def run(self):
        self.outputQueue.put(object(),block=True)
        appLogger.info('init queue...')
#         time.sleep(20)
        while self.__class__.isServer:
            beginTime=time.time()
            processObj=self.process()
            endTime=time.time()
#             if isinstance(processObj,StopSignal):
#                 self.__class__.isServer=False
#                 processObj=None
#                 appLogger.info('%s thread stop' % self.__class__.__name__)
            if isinstance(processObj, StreamLogger):
                processObj.setProcessorLog(self.__class__.__name__,beginTime,endTime)
            if processObj and self.outputQueue:
                if isinstance(processObj,StreamBox):
                    self.__class__.productCount=self.__class__.productCount+1
                if isinstance(processObj,StopSignal):
                    processObj.productCount=self.__class__.productCount
                    self.__class__.isServer=False
                self.outputQueue.put(processObj,block=True)
                
#                 print 'producer put a box in the queue' 
            time.sleep(0.01)
                
if __name__=='__main__':
    obj=IeeeDataProducer()
    obj.run()