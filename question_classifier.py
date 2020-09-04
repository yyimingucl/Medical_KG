# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:03:10 2020

@author: yyimi

Classify the intention from the patient's query
"""

import os
import ahocorasick
from KG_parameters import params
config = params()
#%%

class QuestionClassifier:
    def __init__(self, config):
        #key words
        self.symptoms_lists = [i.strip() for i in open(os.path.join(config.store_path,'symptom.txt')) if i.strip()]
        self.foods_lists = [i.strip() for i in open(os.path.join(config.store_path,'food.txt')) if i.strip()]
        self.parts_lists = [i.strip() for i in open(os.path.join(config.store_path,'part.txt')) if i.strip()]
        self.diseases_lists = [i.strip() for i in open(os.path.join(config.store_path,'disease.txt')) if i.strip()]
        self.departments_lists = [i.strip() for i in open(os.path.join(config.store_path,'department.txt')) if i.strip()]
        self.checks_lists = [i.strip() for i in open(os.path.join(config.store_path,'check.txt')) if i.strip()]
    
        
        self.region_words = set(self.departments_lists + self.diseases_lists + self.checks_lists + self.foods_lists + self.symptoms_lists)
        self.deny_words = [i.strip() for i in open(os.path.join(config.store_path,'deny.txt'), encoding='utf-8') if i.strip()]
        # build actree
        self.region_tree = self.build_actree(list(self.region_words))
        
        # build vocab
        self.wdtype_dict = self.build_wdtype_dict()
        
        # Question key words
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜' ,'忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物','补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']
        self.num_question = 3
        print('model init finished ......')

        return

    def classify(self, question, if_plus = False):
        self.question = question
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {'args':{},'question_types':{}}
        
        data['args'] = medical_dict
        # get the entities in questions
        types = []
        for type_ in medical_dict.values():
            types += type_
            
        question_type = 'others'
        question_types = []
        # Symptom
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)
            
            

        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)
            
        # Cause
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)
            
        # Complication
        if self.check_words(self.acompany_qwds, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)
            
        # Recommend Food
        if self.check_words(self.food_qwds, question) and 'disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)
            
        
        if self.check_words(self.food_qwds+self.cure_qwds, question) and 'food' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'food_not_disease'
            else:
                question_type = 'food_do_disease'
            question_types.append(question_type)
            
        # Disease -> Check List
        if self.check_words(self.check_qwds, question) and 'disease' in types:
            question_type = 'disease_check'
            question_types.append(question_type)
            
        # Check List -> Disease
        if self.check_words(self.check_qwds+self.cure_qwds, question) and 'check' in types:
            question_type = 'check_disease'
            question_types.append(question_type)
            
        #　precaution
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)
            
        # cure period
        if self.check_words(self.lasttime_qwds, question) and 'disease' in types:
            question_type = 'disease_lasttime'
            question_types.append(question_type)
            
        # Disease Treatment
        if self.check_words(self.cureway_qwds, question) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)
            
        # Cure Probability
        if self.check_words(self.cureprob_qwds, question) and 'disease' in types:
            question_type = 'disease_cureprob'
            question_types.append(question_type)
            
            
        # Susceptible People
        if self.check_words(self.easyget_qwds, question) and 'disease' in types :
            question_type = 'disease_easyget'
            question_types.append(question_type)
        
            
            
        # if no query information, return description of disease
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']
            
       
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        # combine results
        data['question_types'] = question_types
        return data

    
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.diseases_lists:
                wd_dict[wd].append('disease')
            if wd in self.departments_lists:
                wd_dict[wd].append('department')
            if wd in self.checks_lists:
                wd_dict[wd].append('check')
            if wd in self.foods_lists:
                wd_dict[wd].append('food')
            if wd in self.symptoms_lists:
                wd_dict[wd].append('symptom')
        return wd_dict

    
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        #search the word i in which region
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}  

        return final_dict

   
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False
    
    def additional_q(self, add_question):
        
        old_question = self.question 
        qwd_sets = self.symptom_qwds+self.cause_qwds+self.acompany_qwds+self.food_qwds+self.drug_qwds+\
        self.prevent_qwds+self.lasttime_qwds+self.cureway_qwds+self.cureprob_qwds+self.easyget_qwds+\
        self.check_qwds+self.belong_qwds+self.cure_qwds
        
        tree = self.build_actree(qwd_sets)
        
        for i in tree.iter(old_question):
            wd = i[1][1]
            old_question = old_question.replace(wd,'')
        
        cur_question = add_question + old_question
        return self.classify(cur_question)
        
        

if __name__ == '__main__':
    handler = QuestionClassifier(config)
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)