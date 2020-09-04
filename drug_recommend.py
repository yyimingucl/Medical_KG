# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 06:33:03 2020

@author: yyimi

Drug Recommend
"""

from py2neo import Graph
from KG_parameters import params
from question_classifier import QuestionClassifier

#%%

class Drug_Searcher():
    
    def __init__(self, res_classify, num_limit = 5):
        self.graph = Graph(
               host="127.0.0.1",
               http_port=7474,
               user="neo4j",
               password="YYMabc990906")    
        self.num_limit = num_limit
        self.res_classify = res_classify
        
    
    def build_entitydict(self, args):
        entity_dict = {}
        subject = []
        for arg, types in args.items():
            subject.append(arg)
            for type_ in types:
                if type_ not in entity_dict:
                    entity_dict[type_] = [arg]
                else:
                    entity_dict[type_].append(arg)
        self.subject = list(set(subject))
        return entity_dict
   
    
    def parser_main(self):
        args = self.res_classify['args']
        entity_dict = self.build_entitydict(args)
        sqls = []
        for type_, entities in entity_dict.items():
            if type_ == 'disease':
                sql = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, n.name, n.taboo, n.prescription_type".format(i) for i in entities]           
                sqls += sql
                
            if type_ == 'symptom':
                sql = ["MATCH (m:Symptom)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, n.name, n.taboo, n.prescription_type".format(i) for i in entities]
                sqls += sql
        
        return sqls
    
    
    def search_main(self):
        sqls = self.parser_main()
        if sqls == []:
            print('没有找到相关药品')
        else:
            return_drug = {'drug':[],'taboo':[]}
            
            for sql_ in sqls:
                answers = []
                ress = self.graph.run(sql_).data()
                answers += ress
                for dict_ in answers:
                    if not self.check_taboo(dict_['n.taboo']) and dict_['n.prescription_type'] != '非 药 品':
                        return_drug['drug'].append(dict_['n.name'])
                        return_drug['taboo'].append(dict_['n.taboo'])
           
            # find intersection of drugs corresponding to all diseases and symptoms        
            final_answer,final_taboo = self.answer_prettify(return_drug)
            print(final_answer)
            print(final_taboo)
            
    
    
    def answer_prettify(self, return_drug):
        desc = list(set(return_drug['drug']))
        taboo = return_drug['taboo']
        subject = self.subject
        max_num = min(len(desc), self.num_limit)
        final_taboo = '药品禁忌:\n'
        if len(desc) != 0:
            final_answer = '针对{0},推荐药品：{1}'.format(';'.join(subject),'; '.join(desc[:max_num]))
            final_taboo += '\n'.join(['[{0}]: {1}'.format(a,b) for a,b in zip(desc[:max_num],taboo[:max_num])])
        else:
            final_answer = ''
        return final_answer,final_taboo
                
            
    def check_taboo(self, taboo):
        for entity in self.res_classify.keys():
            if entity in taboo:
                return True
            else:
                return False
           
        
#%%
if __name__ == '__main__':
    config = params()   
    classifier = QuestionClassifier(config)
    end = False
    while not end:
        query = input('咨询问题:')
        print('='*50)
        print('')
        res_classify = classifier.classify(query)
        d = Drug_Searcher(res_classify)
        d.search_main()
        if input('是否结束:') == '是':
            end = True
        print('='*50)
        print('')
    print('咨询结束')
        
        
        
        
        
        
        