#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 30, 2018

@author: xingtong
'''
import sys,os,time
# project_dir=os.path.dirname(os.path.dirname(__file__))
# print project_dir
# sys.path.append(project_dir)
from logger.LogConfig import appLogger
from processscheduler.ProcessScheduler import ProcessScheduler
# reload(sys)
# sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
#     for module in sys.modules:
#         print module
#     print sys.modules['processscheduler.threadscheduler']
#     print sys.modules['logger.StreamLogger']
    streamLineTemplate=[]
    processQueueSize=50
    streamLineTemplate.append({'QueueSize':50,'pCount':1,'Thread':['bizprocessor.IeeeDataProducer','IeeeDataProducer',1]})
    streamLineTemplate.append({'QueueSize':50,'pCount':1,'Thread':[
#                                                                     ['bizprocessor.GetPdfUrlProcessor','GetPdfUrlProcessor',1]
                                                                    ['bizprocessor.GetRealPdfUrlProcessor','GetRealPdfUrlProcessor',70]
                                                                    ,['bizprocessor.GetPdfFileProcessor','GetPdfFileProcessor',23]
                                                                    ,['bizprocessor.InsertPdfFileIntoMongoDBProcessor','InsertPdfFileIntoMongoDBProcessor',1]
                                                                    ,['bizprocessor.InsertResultIntoMongoDBProcessor','InsertResultIntoMongoDBProcessor',1]
                                                                   ]})
 
     
    processScheduler=ProcessScheduler(streamLineTemplate,processQueueSize)
    processScheduler.execute()