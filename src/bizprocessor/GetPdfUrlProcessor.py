#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 29, 2018

@author: xingtong
'''
from baseprocessor.BaseProcessor import BaseProcessor
from ieeexplorespider.ApiSpider import IeeeApiSpider

def getApiSpider(appConfig):
    apiKey=appConfig.get('ApiSpider','API_KEY')
    queryReturnMaxResult=appConfig.getint('ApiSpider','QUERY_RETURN_MAX_RESULTS')
    maxQueryCountLimit=appConfig.getint('ApiSpider','MAX_QUERY_COUNT_LIMIT')
    queryBeginYear=appConfig.get('ApiSpider','QUERY_BEGIN_YEAR')
    queryEndYear=appConfig.get('ApiSpider','QUERY_END_YEAR')
    return IeeeApiSpider(apiKey,queryReturnMaxResult,maxQueryCountLimit,queryBeginYear,queryEndYear)

class GetPdfUrlProcessor(BaseProcessor):
    '''
    this class is used to get pdf file's url
    '''

    def __init__(self,inputQueue=None,outputQueue=None):
        super(GetPdfUrlProcessor,self).__init__(inputQueue=inputQueue,outputQueue=outputQueue)
        self.apiSpider=getApiSpider(self.appConfig)
            
    def process(self,processObj=None):
        
        if processObj:
#             print 'customer get a box from queue'
            pdfUrl=self.apiSpider.getPdfUrl(processObj.result)
#             print pdfUrl
            processObj.pdfUrl=pdfUrl
        return processObj

if __name__ == '__main__':
    result=[{"_id":"5b839c9b7bbd7112ec94e5bf","issn":"0148-9267","start_page":"106","publication_number":6720219,"rank":16,"article_number":"6792690","title":"&#201;velyne Gayou, Editor: Polychrome Portraits 14: Pierre Schaeffer","abstract_url":"https://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6792690","issue":"1","is_number":6790986,"index_terms":{},"publication_title":"Computer Music Journal","volume":"34","access_type":"LOCKED","content_type":"Journals","authors":{"authors":[{"author_order":1,"affiliation":"San Francisco, California, USA.","full_name":"Thom Blum"}]},"publication_date":"March 2010","fileId":"","publisher":"MIT Press","doi":"10.1162/comj.2010.34.1.106","pdf_url":"https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6792690","partnum":"6792690","end_page":"111","citing_paper_count":0}]
    processObj=GetPdfUrlProcessor()
    processObj.result=result[0]
    obj=GetPdfUrlProcessor()
    obj.process(processObj)
    print processObj.pdfUrl