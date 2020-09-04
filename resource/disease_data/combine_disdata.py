# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 03:00:04 2020

@author: yyimi
"""
import pandas as pd
import os 
#%%
dir_name = os.path.dirname(__file__)
path_1 = os.path.join(dir_name,'disease.csv')
path_2 = os.path.join(dir_name,'disease.json')

def load_disease_json(path): 
    data = pd.read_json(path, encoding='utf-8', lines = True)   
    data['drug'] = data['recommand_drug'] + data['common_drug']
    data = data.drop(columns = ['recommand_drug','common_drug'])
    drug = []
    for item in data['drug']:
        if type(item) != list:
            drug.append(pd.NA)
        else:
            drug.append(list(set(item)))
    data['drug'] = drug
    
    return data

def load_disease_csv(path):
    data = pd.read_csv(path, encoding = 'ANSI')
    return data 


#%% 
large_set = load_disease_csv(path_1)
small_set = load_disease_json(path_2)


#%% form data_set 
cause = []
prevent = []
not_eat = []
do_eat = []
desc = []
pd.set_option('display.max_colwidth',10000)
for name in large_set.name.tolist():
    if name in small_set.name.tolist():
        item = small_set[small_set.name==name]
        cause.append(item['cause'].to_string(index=False))
        prevent.append(item['prevent'].to_string(index=False))       
        do_eat.append(item['do_eat'].tolist()[0])
        not_eat.append(item['not_eat'].tolist()[0])
        desc.append(item['desc'].to_string(index=False))
        
        
    else:
        cause.append(pd.NA)
        prevent.append(pd.NA)
        do_eat.append(pd.NA)
        not_eat.append(pd.NA)
        desc.append(pd.NA)
        
large_set['cause'] = cause
large_set['prevent'] = prevent
large_set['do_eat'] = do_eat
large_set['not_eat'] = not_eat
large_set['desc'] = desc

if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(__file__))
    large_set.to_csv(os.path.join(path,'DISEASE_DATA.csv'),index = False)
    
