# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:08:32 2020

@author: yyimi

Return Relative Information
"""
from KG_parameters import params
from py2neo import Graph
from question_classifier import QuestionClassifier
from paser import QuestionPaser

config = params()
#%%
class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="YYMabc990906")
        self.num_limit = 20

    
    # Carry out sql query, return corresponding result
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        if final_answers == []:
            print('没有查询到相关资料')
        else: 
            print(final_answers)

    # According to question type, return standard pattern
    def answer_prettify(self, question_type, answers):
        final_answer = []
        desc = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            for i in answers:
                if i['n.name']:
                    desc.append(i['n.name'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            for i in answers:
                if i['m.name']:
                    desc.append(i['m.name'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            for i in answers:
                if i['n.cause']:
                    desc.append(i['n.cause'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            for i in answers:
                if i['m.prevent']:
                    desc.append(i['m.prevent'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            for i in answers:
                if i['m.period']:
                    desc.append(i['m.period'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['m.name']
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            for i in answers:
                if i['m.cure_way']:
                    desc.append(i['m.cure_way'])
                else:
                    desc = ['暂无相关资料']
            
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            for i in answers:
                if i['m.cure_rate']:
                    desc.append(i['m.cure_rate'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['m.name']
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            for i in answers:
                if i['m.easy_get']:
                    desc.append(i['m.easy_get'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['m.name']

            final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            for i in answers:
                if i['m.desc']:
                    desc.append(i['m.desc'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['m.name']
            final_answer = '{0},了解一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers if i['n.name']]
            desc2 = [i['m.name'] for i in answers if i['m.name']] 
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            for i in answers:
                if i['n.name']:
                    desc.append(i['n.name'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['m.name']
            final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
            subject = answers[0]['m.name']
            final_answer = '{0}宜食的食物包括有：{1}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers if i['r.name'] == '忌口']
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)


        elif question_type == 'disease_check':
            for i in answers:
                if i['n.name']:
                    desc.append(i['n.name'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            for i in answers:
                if i['m.name']:
                    desc.append(i['m.name'])
                else:
                    desc = ['暂无相关资料']
            subject = answers[0]['n.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer
    
    


if __name__ == '__main__':
    end = False
    handler = QuestionClassifier(config)
    while not end:
        query = input('咨询问题:')
        data = handler.classify(query)
        paser = QuestionPaser()
        sql = paser.parser_main(data)
        searcher = AnswerSearcher()
        searcher.search_main(sql)
        if input('是否结束：') == '是':
            end = True
    print('咨询结束')