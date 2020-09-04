# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 08:21:23 2020

@author: yyimi
"""

import ahocorasick
#%% AC_Automaton
class AC_Automaton(object):
    def __init__(self,string_list):
        self.ac_tree = self.build_actree(string_list)
        
    def build_actree(self,string_list):
        actree = ahocorasick.Automaton()
        
        for index, word in enumerate(string_list):
            actree.add_word(word, (index, word))
            
        actree.make_automaton()
        return actree
    
    def match_medical(self, indication): #indication in drug instruction
        
        region_wds = []
        for i in self.ac_tree.iter(indication):
            word = i[1][1]
            region_wds.append(word)
        
        #if long words contain short words, then pick long words
        compare_set = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    compare_set.append(wd1)
        final_wds = [i for i in region_wds if i not in compare_set]
        
        
        return final_wds

#%%
def load_dict(path):
    '''
    Parameters
    ----------
    path : str
    Returns
    -------
    Dict
    '''
    dic = {}
    with open(path, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            key,values = dictstr_2_dict(line)
            dic[key] = values
    f.close()
    return dic
        

def dictstr_2_dict(string):
    '''
    transform a dict-form string to dict
    Parameters
    ----------
    string : TYPE
        dict form string
    Returns
    -------
    List
    '''
    string = string.rstrip().split(",")
    key = string[0]
    values = []
    if '[]' in string:
        # empty list 
        return key, values
    else:
        string[1] = string[1].replace('[','')
        string[-1] = string[-1].replace(']', '')
        for each in string[1:]:
            values.append(each.replace('\'','').lstrip())
        return key, values
                    
        
#%% 
def list2str(word_list):
    """
    Parameters
    ----------
    word_list : LIST
        The List contains several key words 
    Returns
    -------
    string split the keywords by space
    """
    if len(word_list) == 1:
        return ''.join(word_list)
    else:
        return ' '.join(word_list)
    
    
#%%   
    
def extract_num(string):
    '''
    extract age from describtion of patient
    Parameters
    ----------
    string : str
    Returns
    -------
    number in string
    '''
    next_word = False    
    number = ''
    ch_number = ''
    res = []
    ch2num = {'一':1,'二':2,'三':3,'四':4,
              '五':5,'六':6,'七':7,'八':8,
              '九':9,'十':10}
    for i in range(len(string)):
        if string[i].isdigit() and not next_word:
            number += string[i]
            if string[i+1].isdigit():
                next_word = False
            else:
                next_word = True
                res.append(int(number))
                number = ''
                
    next_word = False
    for i in range(len(string)):     
        if string[i] in ch2num.keys() and not next_word:
            ch_number += string[i]
            if string[i+1] in ch2num.keys():
                next_word = False
            else:
                next_word = True
                res.append(chage_num(ch_number))
                ch_number = ''
            
    return res




def chage_num(chinese_number):
    '''
    transefer age (under 200) in capital Chinese to int
    Parameters
    ----------
    chinese_number : string
    
    Returns
    -------
    num : int
    '''
    ch2num = {'一':1,'二':2,'两':2,'三':3,'四':4,
              '五':5,'六':6,'七':7,'八':8,
              '九':9,'十':10,'百':100}
    digit = {'十':1,'百':2}
    if len(chinese_number) == 1:
        #1-9
        return ch2num[chinese_number]
    
    if chinese_number[0] == '十':
        #11-19
        return 10+ch2num[chinese_number[1]]
    
    else:
        #others
        num = 0
        i = len(chinese_number) - chinese_number.count('十') - chinese_number.count('百')
        if chinese_number[-1] in digit.keys():
            i += digit[chinese_number[-1]]
        for char in chinese_number:
            if char in digit.keys():
                continue
            else:
                i-=1
                num += ch2num[char]*(10**i)
                
        return num 
        
    
    
#%%


   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    