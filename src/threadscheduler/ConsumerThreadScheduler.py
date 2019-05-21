#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 30, 2018

@author: xingtong
'''
import sys,time
from Queue import Queue
from logger.LogConfig import appLogger
from baseprocessor.FirstProcessor import FirstProcessor
from baseprocessor.LastProcessor import LastProcessor
from baseprocessor.BaseProcessor import BaseProcessor
import os
import bizprocessor.GetPdfUrlProcessor
import bizprocessor.GetRealPdfUrlProcessor
import bizprocessor.GetPdfFileProcessor
import bizprocessor.InsertPdfFileIntoMongoDBProcessor
import bizprocessor.InsertResultIntoMongoDBProcessor


class ConsumerThreadScheduler(object):
    def __init__(self,streamLineTemplate,inputQueue=None,outputQueue=None):
        self.streamLineTemplate=streamLineTemplate
        self.inputQueue=inputQueue
        self.outputQueue=outputQueue
        
    def CreateSteamLine(self):
        '''
       create a streamline
        @return:  a list which contains all bizprocessors(business processors) the list's structure like this: first processors->bizprocessors->last processors
        '''
        streamLineArray=[]
        if self.streamLineTemplate:
            queueSize=self.streamLineTemplate.get('QueueSize')
            itemList=self.streamLineTemplate.get('Thread')
            inputQueue=None
            outputQueue=Queue(maxsize=queueSize)
            for i in xrange(1):
                firstProcessor=FirstProcessor(self.inputQueue,outputQueue)
                streamLineArray.append(firstProcessor)    #add the first processor
            for item in itemList:  #add bizprocessors
                tCount=item[-1]
                if tCount:
                    if outputQueue:
                        inputQueue=outputQueue
                    else:
                        inputQueue=Queue(maxsize=queueSize)
                    outputQueue=Queue(maxsize=queueSize)
                    module=sys.modules[item[0]]  
                    cClass=getattr(module, item[1])
                    for i in range(tCount):
                        cObj=cClass(inputQueue=inputQueue,outputQueue=outputQueue)
                        cObj.domean=True
                        streamLineArray.append(cObj)
            for i in xrange(1):
                lastProcessor=LastProcessor(outputQueue,self.outputQueue)
                streamLineArray.append(lastProcessor)  #add the last processor
        return streamLineArray
    
    def execute(self):
        '''
        the main function to execute software
        '''
        #create streamline
        streamLineArray=self.CreateSteamLine()
        #start each bizprocessor in the streamline
        for item in streamLineArray:
            if isinstance(item,BaseProcessor):
                item.start()
        while True:
            time.sleep(0.01)
        appLogger.info('%s thread stop' % self.__class__.__name__)           