#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 24, 2018

@author: xingtong
'''

from xploreapi import XPLORE
from logger.LogConfig import appLogger
import json



'''
Key Rate Limits
10    Calls per second
200    Calls per day
'''
class IeeeApiSpider(object):
    API_KEY=r'mghspz84xgsy6sawfgn3tm7k'
    QUERY_RETURN_MAX_RESULTS=5  #max is 200
    MAX_QUERY_COUNT_LIMIT=2
    TOTAL_MAX_RESULTS=0
    CUR_QUERY_COUNT=0  #current query count
    QUERY_BEGIN_YEAR=None
    QUERY_END_YEAR=None
    
    def __init__(self,apiKEY=None,queryReturnMaxResult=0,maxQueryCountLimit=0,queryBeginYear=None,queryEndYear=None):
        if apiKEY:
            self.API_KEY=apiKEY
        if queryReturnMaxResult:
            self.QUERY_RETURN_MAX_RESULTS=queryReturnMaxResult
        if maxQueryCountLimit:
            self.MAX_QUERY_COUNT_LIMIT=maxQueryCountLimit
        if queryBeginYear:
            self.QUERY_BEGIN_YEAR=queryBeginYear
        if queryEndYear:
            self.QUERY_END_YEAR=queryEndYear
        self.TOTAL_MAX_RESULTS=self.MAX_QUERY_COUNT_LIMIT*self.QUERY_RETURN_MAX_RESULTS
    
    def getQueryInfo(self, keyWord=''):
        '''
        get query info
        '''
        sReturn='key word: %s ; query begin year: %s ; query end year: %s ; open access: True' % (keyWord,self.QUERY_BEGIN_YEAR,self.QUERY_END_YEAR)
        return sReturn
    
    def queryData(self, keyWords=''):
        '''
        query ieee xplore database to get results
        @param keyWords: key words
        @return: a list which contains query results, and every result is the json formate. The max results count is 40000  
        '''
#         lReturn=[{"_id":"5b839c9b7bbd7112ec94e5bf","issn":"0148-9267","start_page":"106","publication_number":6720219,"rank":16,"article_number":"6792690","title":"&#201;velyne Gayou, Editor: Polychrome Portraits 14: Pierre Schaeffer","abstract_url":"https://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6792690","issue":"1","is_number":6790986,"index_terms":{},"publication_title":"Computer Music Journal","volume":"34","access_type":"LOCKED","content_type":"Journals","authors":{"authors":[{"author_order":1,"affiliation":"San Francisco, California, USA.","full_name":"Thom Blum"}]},"publication_date":"March 2010","fileId":"","publisher":"MIT Press","doi":"10.1162/comj.2010.34.1.106","pdf_url":"https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6792690","partnum":"6792690","end_page":"111","citing_paper_count":0}]
        lReturn=[]
        try:
            begin=1  #query start record number
            query=XPLORE(self.API_KEY)
            query.maximumResults(self.QUERY_RETURN_MAX_RESULTS)
            query.queryText(keyWords)
            query.resultsSorting('publication_year','desc')
#             query.resultsFilter('content_type','Journals')  #only query journals
            query.resultsFilter('open_access','True')  #only query the articles which is open access
            if self.QUERY_BEGIN_YEAR:
                query.resultsFilter('start_year',self.QUERY_BEGIN_YEAR)
            if self.QUERY_END_YEAR:
                query.resultsFilter('end_year', self.QUERY_END_YEAR) 
#             appLogger.info(self.getQueryInfo(keyWords))
            while True:
                query.startingResult(begin)
                results = query.callAPI(debugModeOff=True)
#                 print results
                self.CUR_QUERY_COUNT+=1
                articles=self.getArticles(results)  #get articles list
                if articles:
                    lReturn.extend(articles)  # add articles to result list
                    size=len(articles)  #get query total number
                    if size==self.QUERY_RETURN_MAX_RESULTS and self.CUR_QUERY_COUNT<self.MAX_QUERY_COUNT_LIMIT:  #if still has more articles,continue query
                        begin=len(lReturn)+1
                    else:
                        break
                else:
                    break
        except Exception, err:
            appLogger.error(err)
        return lReturn
    
    def getArticles(self, jsonResponse):
        '''
        get query articles
        @param jsonResponse: the query results which are from ieee xplore database
        @return: a list which contains article data 
        '''
        pReturn=None
        try:
            if jsonResponse:
                jdatas=json.loads(jsonResponse)
                if jdatas:
                    pReturn=jdatas.get('articles')
        except Exception, err:
            appLogger.error(err)
        return pReturn
    
    def getPdfUrl(self, jsonResult):
        '''
        get pdf file url from article data
        @param jsonResult: article data which is json format
        @return: the pdf url of the article
        '''
        uReturn=None
        try:
            if jsonResult:
                uReturn=jsonResult['pdf_url']
        except Exception,err:
            appLogger.error(err)
        return uReturn

    
if __name__ == '__main__':
    keyWords=r'sworm'
#     query=XPLORE(r'mghspz84xgsy6sawfgn3tm7k')
#     query.queryText(keyWords)
#     print query.callAPI()  
    idf=IeeeApiSpider()
    for itr in idf.queryData(keyWords):
        print itr

    