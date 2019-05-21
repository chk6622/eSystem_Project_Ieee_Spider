#!/usr/bin/env python
#coding: utf-8
'''
Created on Sep 19, 2018

@author: xingtong
'''

import numpy as np
import abs.ObjFunction as ObjFunction


class ABSIndividual:

    '''
    individual of artificial bee swarm algorithm
    '''

    def __init__(self,  vardim, bound):
        '''
        vardim: dimension of variables
        bound: boundaries of variables
        '''
        self.vardim = vardim
        self.bound = bound
        self.fitness = 0.
        self.trials = 0

    def generate_bak(self):
        '''
        generate a random chromsome for artificial bee swarm algorithm
        '''
        len = self.vardim
        rnd = np.random.random(size=len)
        self.chrom = np.zeros(len)
        for i in xrange(0, len):
            self.chrom[i] = self.bound[0, i] + \
                (self.bound[1, i] - self.bound[0, i]) * rnd[i]
                
    def generate(self):
        '''
        generate a random chromsome for artificial bee swarm algorithm
        '''
        len = self.vardim
        rnd = np.random.random(size=len)
        self.chrom = np.zeros(len)
        bottom=self.bound[0,0]
        ceiling=self.bound[1,0]
        for i in xrange(0, len):
            self.chrom[i]=np.random.randint(bottom,(ceiling-(len-1)))
            ceiling-=self.chrom[i]
            len-=1
#         print self.chrom
            

    def calculateFitness(self):
        '''
        calculate the fitness of the chromsome
        '''
#         self.fitness = ObjFunction.GrieFunc(
#             self.vardim, self.chrom, self.bound)
        
        self.fitness = ObjFunction.getPipelineFuncFitness(self.vardim, self.chrom)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        