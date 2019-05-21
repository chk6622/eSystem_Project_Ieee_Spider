#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 21, 2018

@author: xingtong
'''
import requests
import cookielib
import urllib

class A(object):
    attr=1
    
    def fun(self):
        A.attr=3
    
print A.attr

A.attr=2

print A.attr

a=A()
a.fun()

print A.attr