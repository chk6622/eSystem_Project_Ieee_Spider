#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 28, 2018

@author: xingtong
'''

import os
import logging.config

BASE_DIR=BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.config.fileConfig(os.path.join(BASE_DIR,'log','../logging.conf'))
appLogger = logging.getLogger("IeeexploreSpider")