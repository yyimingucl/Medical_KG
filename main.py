# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 07:42:30 2020

@author: yyimi
"""

from searcher import AnswerSearcher
from drug_recommend import Drug_Searcher
from KG_parameters import params
from question_classifier import QuestionClassifier
from paser import QuestionPaser

#%%
if __name__ == '__main__':
    config = params()
    handler = QuestionClassifier(config)
    end = False
    while not end:
        query = input('咨询问题:')
        print('')
        res_classify = handler.classify(query)
        paser = QuestionPaser()
        
        sql = paser.parser_main(res_classify)
        searcher = AnswerSearcher()
        searcher.search_main(sql)
        print('')
        print('---------------  药品推荐  ---------------')
        print('')
        d = Drug_Searcher(res_classify)
        d.search_main()
        print('')
        if input('针对该问题是否需要追加提问:') in ['是','需要']:
            new_query = input('查询问题:')
            res_classify = handler.additional_q(new_query)
            sql = paser.parser_main(res_classify)
            searcher.search_main(sql)
                 
        if input('是否结束:') == '是':
            end = True
        print('='*50)
        print('')
    print('咨询结束')
        
        
        
        
        