#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 22, 2018

@author: xingtong
'''

import pymongo
import bson.binary
from bson.objectid import ObjectId
from pymongo import MongoClient
from cStringIO import StringIO
import types 
from hamcrest.core.core.isnone import none
from bson.objectid import ObjectId
from logger.LogConfig import appLogger
import os

class MongoDBDAO:
    DB_NAME = r'test1'
    DB_HOST = r'cluster0-hxejh.mongodb.net/'
    DB_PORT = 27017
    DB_USER = r'user1' 
    DB_PASS = r'''xhy121230'''
    DB_URL=''
    DB_CLIENT=None
    DB_COLL='test_colle'  # the collection which stores normal data
    DB_COLL_BIN='test_bin_colle'  # the collection which stores binary data
    
    def __init__(self, dbName=None, dbHost=None, dbPort=None, dbUser=None, dbPass=None, dbColl=None, dbBinColl=None):
        self.initUrl()
        self.DB_CLIENT=self.getDatabase(dbName)
        if dbName:
            self.DB_NAME=dbName
        if dbHost:
            self.DB_HOST=dbHost
        if dbPort:
            self.DB_PORT=dbPort
        if dbUser:
            self.DB_USER=dbUser
        if dbPass:
            self.DB_PASS=dbPass
        if dbColl:  #init normal collection
            self.DB_COLL=dbColl
        if dbBinColl:  #init data collection
            self.DB_COLL_BIN=dbBinColl
        
    def initUrl(self):
        '''
        init the connection url of mongoDB
        '''
        self.DB_URL+=r'''mongodb+srv://'''
        self.DB_URL+=self.DB_USER
        self.DB_URL+=r''':'''
        self.DB_URL+=self.DB_PASS
        self.DB_URL+=r'''@'''
        self.DB_URL+=self.DB_HOST
        
    def getDatabase(self, databaseName):  
        '''
        get the database of mongoDB
        @param databaseName:the name of database
        @return: the database which name is databaseName, if the database does not exist return None 
        '''     
        if databaseName:
            try:
                client = MongoClient(self.DB_URL)
                databaseNames=client.database_names()
                if databaseName in databaseNames:   
                    return client[databaseName]
            except Exception, err:
                appLogger.error(err)
        return None
    
    def getCollection(self, collectionName):
        '''
        get the collection of the mongoDB
        @param collectionName: the name of the collection
        @return: the collection which name is collectionName, if the collection does not exist return None
        '''
        if collectionName and self.DB_CLIENT:
            try:
                return self.DB_CLIENT[collectionName]
            except Exception, err:
                appLogger.error(err)
        return None
            
    def insertOneData(self, collectionName=DB_COLL, **dataSet):
        '''
        insert data into the mongoDB
        @param collectionName: : collection name of the database
        @param dataSet:BSON data which will be inserted into the mongoDB
        @return:  if insert success return id which is in the mongoDB, else return None 
        '''
        sReturn=None
        try:
            if dataSet and collectionName:
                coll=self.getCollection(collectionName)
                if coll:
                    resultObject = coll.insert_one(dataSet)
                    if resultObject:
                        sReturn=resultObject.inserted_id
        except Exception, err:
            appLogger.error(err)
        return sReturn
        
    def insertFile(self, filePath, saveFilename, collectionName=DB_COLL_BIN, isDelFile=False):
        '''
        insert file into the mongodb
        @param filePath: file path which will be inserted
        @param saveFilename: file name which is in the mongodb
        @param collectionName: collection name of the database
        @param isDelFile: if true then delete the file which is filePath
        @return: if insert success return id which is in the mongoDB, else return None 
        '''
        sReturn=None
        try:
            if filePath:
                filePath=filePath.decode('utf-8')
                with open (filePath,'rb') as fileObj:
                    content = StringIO(fileObj.read())
                    sReturn=self.insertBinaryData(content.getvalue(), saveFilename, collectionName)
            
        except Exception, err:
            appLogger.error(err)
        finally:
            if isDelFile:
                try:
                    os.remove(filePath)
                except Exception, err:
                    appLogger.error(err)
        return sReturn

                    
    def insertBinaryData(self,binaryData,saveFilename,collectionName):
        '''
        insert binary data into the mongodb
        @param binaryData: binary data which will be inserted
        @param saveFilename: file name which is in the mongodb
        @param collectionName: collection name of the database
        @return: if insert success then it will return id which is in the mongoDB, else return None 
        '''
        sReturn=None
        try:
            if binaryData:
                coll=self.getCollection(collectionName)
                if coll:
                    sReturn = coll.save(dict(content= bson.binary.Binary(binaryData),filename = saveFilename))
        except Exception, err:
            appLogger.error(err)
        return sReturn
            

    def getFileById(self,fileId,collectionName):
        '''
        get binary data from mongodb
        @param fileId: the id of file which will get from the MongoDB
        @param collectionName: collection name of the database
        @return: the file data which is stored in the mongoDB 
        '''
        dReturn=None
        try:
            if fileId:
                coll=self.getCollection(collectionName)
                data = coll.find_one({'_id':ObjectId(fileId)})
                if data:
                    dReturn=data['content']
        except Exception, err:
            appLogger.error(err)
        return dReturn
#             if data:
#                 if savePath:
#                     out = open(savePath.decode('utf-8'),'wb')
#                     out.write(data['content'])
#                     out.close()
                    
if __name__ == '__main__':
    dao=MongoDBDAO()
    dataSet={'data1':'val1','data2':'val2'}
    print dao.insertOneData('test_colle',**dataSet)
#     dao.insertFile('C:\\Users\\xingtong\\Downloads\\export2018.08.06-03.13.04.csv','export2018.08.06-03.13.04.csv','test_colle')
#     filedata=dao.getFileById('5b7e7f147bbd712c78605c01', 'test_colle')
#     print filedata
#     filedata=dao.getFileById('5b7e7f457bbd712b1cdcf862', 'test_colle')
#     print filedata
#     filedata=dao.getFileById('5b7e7f837bbd712d7cc66252', 'test_colle')
#     print filedata
    