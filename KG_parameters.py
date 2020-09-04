# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 09:00:39 2020

@author: yyimi
"""

import argparse
import numpy as np
import random
import os
#%%
def set_manual_seed(seed):
    random.seed(seed)
    np.random.seed(seed)    
set_manual_seed(70)
print("设置随机数种子为70")

#%%

root_path = os.path.dirname(os.path.abspath(__file__))

def params():
    parser = argparse.ArgumentParser()
    add_arg = parser.add_argument
    #Data path
    add_arg("--vocab",default=os.path.join(root_path+'\\resource','vocab.txt'), 
            help = "external vocab for jieba", type = str)
    add_arg("--disease_data",default=os.path.join(root_path+'\\resource','DISEASE_DATA.csv'), 
            help = "disease data to build knowledge graph", type = str)
    add_arg("--relation_path",default=os.path.join(root_path+'\\resource','relation.csv'), 
            help = "relation between drug and disease", type = str)
    add_arg('--store_path', default=root_path+'\\resource', 
            help = 'store the processing data')
    
    
    #URL
    add_arg("--url",default='https://www.jiankangle.com/healthMall/category;jsessionid=FDC570E85A0BE68990B51FAB6307B454', 
            help = "obtain the drug category structure from web", type = str)
    

    
    
            
    args = parser.parse_args()
    return args