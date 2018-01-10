# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
import time
import logging
import os

class Log:

    def __init__(self,path):
        self.path = path
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
 
        # create a file handler
        handler = logging.FileHandler(path+'/log.log')
        handler.setLevel(logging.INFO)
 
        # create a logging format
        
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        
        # add the handlers to the logger
        
        logger.addHandler(handler)
        self.logger = logger
    def record(self,msg,output):
        if output:
            print(msg)
        self.logger.info(msg)
        