# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 07:40:11 2020

@author: yyimi

Build Knowledge Graph by NEO4J(Baesd on Disease)
"""

from py2neo import Graph, Node
import re,os,ast
from KG_parameters import params
from KG_functions import load_dict,list2str
from KG_data import load_disease_data, load_medicine_data
from jkl_url.jkl_url import Navigation
import pandas as pd 
pd.set_option('display.max_colwidth',10000)

#%%
class MedicalGraph(object):
    def __init__(self, config):
        self.disease_data = load_disease_data(config.disease_data)
        self.medicine_data = load_medicine_data()
        self.disease2drug = load_dict(config.relation_path)
        self.drug_structure = Navigation(config.url)
        self.graph = Graph("http://localhost:7474", username="neo4j", password="YYMabc990906")
        self.store_path = config.store_path
        
    def read_nodes(self):
        # 9 entity nodes
        category_drug = [] #category of drug 
        checks = [] # check
        departments = [] # department
        symptoms = [] # symptom
        foods = [] #food
        diseases = []
        parts = [] 
        
        # store the attibutes of drug node and disease node
        disease_infos = {} # disease information 
        drug_infos = {} #drug inforamtion 
        
        
        # relationship between nodes
        rels_department = [] #　科室－科室关系
        rels_drug = [] # 疾病－热门药品关系
        rels_check = [] # 疾病－检查关系
        rels_category = [] # big&small categroies of drug 
        rels_drug_category = [] #drug name and categories 
        rels_symptom = [] # disease and symptom
        rels_complication = [] # disease and complication
        rels_dis_department = [] #　disease and department
        rels_symptom_drug = [] # drug and symptom
        rels_parts = []
        rels_noteat = [] # 疾病－忌吃食物关系
        rels_doeat = [] # 疾病－宜吃食物关系
        
        # Fill Disease Data
        pattern = u'[^\u4e00-\u9fa5_a-zA-Z]'
        regex = re.compile(pattern)
        count = 0
        print('start filling medicine data') 
        for each in self.disease_data.iterrows():
            # each is in form (index, (content in one row of dataframe))
            count += 1
            print(count)
            disease = each[1][0] # disease(1)
            desc = each[1][-1] # desc(-1)
            part = each[1][2] # part(2)
            easy_get = each[1][3] # easy_get(3) 
            departms = each[1][6] # department(6)
            prevent = each[1][21] # prevent(21)
            cause = each[1][20] # cause(20)
            symptom = each[1][8] # symptom(8)
            insurance = each[1][5] #insurance(5)
            infection = each[1][4] # infection(4)
            complication = each[1][9] # complication(9)
            cure_way = each[1][10] # cure_way(10)
            period = each[1][12] # period(12)
            cure_rate = each[1][13] #cure_rate(13)
            money = each[1][14] # money(14)
            check_list = each[1][7] # check_list(7)
            easy_get = each[1][18] # age(18)
            do_eat = each[1][22] #do_eat(22)
            not_eat = each[1][23] #not_eat(23)
            
            diseases.append(disease)
            disease_infos[disease] = {'desc':'', 'cause':'','infection':'',
                                      'insurance':'', 'period':'', 'prevent':'',
                                      'get_rate':'', 'cure_way':'', 'money':'',
                                      'cure_rate':'', 'easy_get':''}
            # disease and part 
            if part != -1:
                part_tmp = part.split()
                for p_ in part_tmp:
                    parts.append(p_)
                    rels_parts.append([disease,part])
                
            # disease and food
            if do_eat != -1 :
                do_eat = ast.literal_eval(do_eat)
                for item in do_eat:
                    foods.append(item)
                    rels_doeat.append([disease,item])
                    
            if not_eat != -1:
                not_eat = ast.literal_eval(not_eat)
                for item in not_eat:
                    foods.append(item)
                    rels_noteat.append([disease,item])
                    
            # disease and symptom
            if symptom != -1:
                symptom = symptom.split()[:-1]
                for item in symptom:
                    rels_symptom.append([disease, item])
                    symptoms.append(item)
                    for drug in self.disease2drug[disease]:
                        rels_symptom_drug.append((item,drug))
                
                
            # disease and complications
            if complication != -1:
                complication = complication.split()[:-1]
                for item in complication:
                    rels_complication.append([disease,item])
                    
            
            # rels_department and rels_dis_departments
            if departms != -1:
                departms = departms.split()
                if len(departms) == 1:
                    rels_dis_department.append([disease,departms[0]])
                    departments.append(departms[0])          
                if len(departms) == 2:
                    big, small = departms
                    rels_department.append([big,small])
                    rels_dis_department.append([disease,small])
                    departments.append(big)
                    departments.append(small)
            
            
            # check_list and disease
            if check_list != -1:
                check_list = check_list.split()[:-1]
                for item in check_list:
                    rels_check.append([disease,item])
                    checks.append(item)
            
            
            #drugs and disease rels_drug
            if self.disease2drug[disease] != []:        
                for drug in self.disease2drug[disease]:
                    rels_drug.append([disease,drug])
            else:
                drug = '暂无相关药品'
                rels_drug.append([disease,drug])
                
                    
            #print([disease,drug])
            
            
            #cure_way
            if cure_way != -1 :
                disease_infos[disease]['cure_way'] += ''.join(cure_way)
            else:
                disease_infos[disease]['cure_way'] += '暂无相关资料'
                
            #cause
            if cause != -1 :
                disease_infos[disease]['cause'] += cause
            else:
                disease_infos[disease]['cause'] += '暂无相关资料'
                
            #prevent 
            if prevent != -1 :
                disease_infos[disease]['prevent'] += prevent
            else:
                disease_infos[disease]['prevent'] += '暂无相关资料'
            
            #desc
            if desc != -1 :
                disease_infos[disease]['desc'] += desc
            else:
                disease_infos[disease]['desc'] += '暂无相关资料'
            
            
            #easy_get_people 
            if easy_get != -1 :
                disease_infos[disease]['easy_get'] += easy_get
            else:
                disease_infos[disease]['easy_get'] += '暂无相关资料'
            
                
            #infection 
            if infection != -1 :
                disease_infos[disease]['infection'] += infection
            else:
                disease_infos[disease]['infection'] += '暂无相关资料'
            
            #insurance
            if insurance != -1 :
                disease_infos[disease]['insurance'] += insurance
            else:
                disease_infos[disease]['insurance'] += '暂无相关资料'
            
            #period
            if period != -1 :
                disease_infos[disease]['period'] += period
            else:
                disease_infos[disease]['period'] += '暂无相关资料'
            
            
            
            #cure_rate
            if cure_rate != -1 :
                disease_infos[disease]['cure_rate'] += str(cure_rate)
            else:
                disease_infos[disease]['cure_rate'] += '暂无相关资料'
                
            #money
            if money != -1 :
                disease_infos[disease]['money'] += money
            else:
                disease_infos[disease]['money'] += '暂无相关资料'
        print('--------Complete Fill Disease Data--------')
        
        count = 0
        print('--------Start Filling Medicine Data--------')                      
        #Fill Drug Data
        
        for each in self.medicine_data.iterrows():
            count+=1
            print(count)
            
            ids = each[1][0] # id(0) 
            class_info = each[1][1] # class_info(1)
            brand = each[1][4] # brand(4)
            name = each[1][5] # goods_name(6)
            producer = each[1][16] # manufacturer(16)
            bad_reaction = each[1][20] # adverse_drug_reactions(20)
            taboo = each[1][24] # taboo(24)
            us_dos = each[1][28] # usage and dosage(28)
            interaction = each[1][31] # interactions(31)
            ingredient = each[1][33] # ingredients(33)
            prescription_type = each[1][48] # prescription_type(48)
            


            
            drug_infos[name] = {'producer':'','taboo':'',
                               'prescription_type':'','ingredients':'',
                               'interactions':'','-drug_reaction':'',
                               'usage&dosage':'','brand':'',
                               'ids':''}
            
            # name
            drug_infos[name]['ids'] += list2str(regex.sub('',ids).strip())
            
            #producer
            if producer != -1:
                drug_infos[name]['producer'] += producer
            else:
                drug_infos[name]['producer'] += '暂无相关资料'
                
            #brand
            if brand != -1:
                drug_infos[name]['brand'] += brand
            else:
                drug_infos[name]['brand'] += '暂无相关资料'
            
            #taboo
            if taboo != -1:
                drug_infos[name]['taboo'] += taboo
            else:
                drug_infos[name]['taboo'] += '暂无相关资料'
            
            #prescription type
            if prescription_type != -1:
                drug_infos[name]['prescription_type'] += prescription_type
            else:
                drug_infos[name]['prescription_type'] += '暂无相关资料'
            
            #interactions
            if interaction != -1:
                drug_infos[name]['interactions'] += interaction
            else:
                drug_infos[name]['interactions'] += '暂无相关资料'
            #ingredients
            if ingredient != -1:
                drug_infos[name]['ingredients'] += ingredient
            else:
                drug_infos[name]['ingredients'] += '暂无相关资料'
                
            #
            if bad_reaction != -1:
                drug_infos[name]['-drug_reaction'] += bad_reaction
            else:
                drug_infos[name]['-drug_reaction'] +='暂无相关资料'
            
            #usage&dosage
            if us_dos != -1:
                drug_infos[name]['usage&dosage'] += us_dos
            else:
                drug_infos[name]['usage&dosage'] += '暂无相关资料'
            
            if class_info in self.drug_structure.keys():
                big,small = self.drug_structure[class_info]
                category_drug.append(big)
                category_drug.append(small)
                rels_category.append([small,big])
                rels_drug_category.append([name, small])
            else:
                category_drug.append(class_info)
                rels_drug_category.append([name, class_info])
        print('-----------Complete Filling Medicine Data------------')
        
        return set(parts), set(category_drug),set(checks),set(departments),set(symptoms),\
        set(foods),set(diseases),disease_infos,drug_infos,rels_department,rels_drug,rels_category,rels_check,\
        rels_category,rels_drug_category,rels_symptom,rels_complication,rels_dis_department,set(rels_symptom_drug),\
        rels_noteat, rels_doeat,rels_parts
    
    
    
    def create_node(self, label, nodes):
        #build nodes
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.graph.create(node)
            count += 1
            print(count, len(nodes))
        return
        
    
    def create_diseases_nodes(self, disease_infos):
        #build disease node
        count = 0
        for disease_name, disease_dict in disease_infos.items():
            node = Node("Disease", name = disease_name, 
                        desc = disease_dict['desc'],
                        cause = disease_dict['cause'],
                        prevent = disease_dict['prevent'],
                        infection = disease_dict['infection'],
                        period=disease_dict['period'],
                        easy_get=disease_dict['easy_get'],
                        insurance = disease_dict['insurance'],
                        money = disease_dict['money'], 
                        get_rate = disease_dict['get_rate'],
                        cure_rate = disease_dict['cure_rate'],
                        cure_way = disease_dict['cure_way'])
            self.graph.create(node)
            count += 1
            print(count)
        print('--------Complete Create Disease Node--------')
        return
    
    def create_medicine_nodes(self, medicine_infos):
        #build medicine node
        count = 0
        for drug_name, medicine_dict in medicine_infos.items():
            node = Node("Drug", name = drug_name,
                        ids = medicine_dict['ids'], 
                        taboo = medicine_dict['taboo'],
                        prodcuer = medicine_dict['producer'], 
                        brand = medicine_dict['brand'],
                        interactions = medicine_dict['interactions'], 
                        ingredients = medicine_dict['ingredients'],
                        drug_reaction = medicine_dict['-drug_reaction'],
                        prescription_type = medicine_dict['prescription_type'], 
                        usage_dosage = medicine_dict['usage&dosage'])
            self.graph.create(node)
            count += 1
            print(count)
        print('-------Complete Create Medicine Node-------')
        return
    
    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        parts, category_drug,checks,departments,symptoms,foods,diseases,disease_infos,drug_infos,rels_department,rels_drug,rels_category,rels_check,rels_category,rels_drug_category,rels_symptom,rels_complication,rels_dis_department,rels_symptom_drug,rels_noteat,rels_doeat,rels_parts = self.read_nodes()
        
        self.create_diseases_nodes(disease_infos)
        self.create_medicine_nodes(drug_infos)
        
        self.create_node('Part',parts)
        print('number of part nodes{a}'.format(a = len(parts)))
        self.create_node('Food',foods)
        print('number of food nodes{a}'.format(a = len(foods)))
        self.create_node('Check', checks)
        print('number of check nodes{a}'.format(a = len(checks)))
        self.create_node('Department', departments)
        print('number of department nodes{a}'.format(a = len(departments)))
        self.create_node('Symptom', symptoms)
        print('number of symptom nodes{a}'.format(a = len(symptoms)))
        self.create_node('Category_of_Drug', category_drug)
        print('number of categories of drug nodes{a}'.format(a = len(category_drug)))
        return
    
    '''创建实体关系边'''
    def create_graphrels(self):
        #Build relationship between entities 
        
        parts, category_drug,checks,departments,symptoms,foods,diseases,disease_infos,drug_infos,rels_department,rels_drug,rels_category,rels_check,rels_category,rels_drug_category,rels_symptom,rels_complication,rels_dis_department,rels_symptom_drug,rels_noteat,rels_doeat,rels_parts = self.read_nodes()
        self.create_relationship('Disease', 'Part', rels_parts, 
                                 'happen_on', '发生部位')
        
        self.create_relationship('Disease', 'Check', rels_check, 
                                 'check_list', '诊断检查')
        self.create_relationship('Department', 'Department', rels_department, 
                                 'includes', '包括')
        self.create_relationship('Disease', 'Drug', rels_drug, 
                                 'common_drug', '常用药品')
        self.create_relationship('Category_of_Drug','Category_of_Drug', rels_category,
                                 'belongs_to', '属于')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 
                                 'has_symptom', '症状')
        self.create_relationship('Disease', 'Department',rels_dis_department, 
                                 'belongs_to', '所属科室')
        self.create_relationship('Disease', 'Disease', rels_complication,
                                 'acompany_with', '并发症')
        self.create_relationship('Disease', 'Food', rels_doeat,
                                 'do_eat', '宜吃')
        self.create_relationship('Disease', 'Food', rels_noteat,
                                 'not_eat', '忌口')
        self.create_relationship('Symptom', 'Drug', rels_symptom_drug, 
                                 'common_drug', '常用药品')
        self.create_relationship('Drug', 'Category_of_Drug',rels_drug_category,
                                 'belongs_to', '属于')                        
        
        print('---------Complete Create RelationShip Edges---------')
        print('---------Knowledge Graph Has been Builded----------')
    
    
    
    
    
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.graph.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return
    
    
    def export_data(self):
        parts,category_drug,checks,departments,symptoms,foods,diseases,disease_infos,drug_infos,rels_department,rels_drug,rels_category,rels_check,rels_category,rels_drug_category,rels_symptom,rels_complication,rels_dis_department,rels_symptom_drug,rels_noteat,rels_doeat,rels_parts = self.read_nodes() 
        
        f_check = open(os.path.join(self.store_path,'check.txt'), 'w+')
        f_department = open(os.path.join(self.store_path,'department.txt'), 'w+')
        f_symptom = open(os.path.join(self.store_path,'symptom.txt'), 'w+')
        f_disease = open(os.path.join(self.store_path,'disease.txt'), 'w+')
        f_food = open(os.path.join(self.store_path,'food.txt'), 'w+')
        f_part = open(os.path.join(self.store_path,'part.txt'), 'w+')
        
        f_check.write('\n'.join(list(checks)))
        f_department.write('\n'.join(list(departments)))
        f_symptom.write('\n'.join(list(symptoms)))
        f_disease.write('\n'.join(list(diseases)))
        f_food.write('\n'.join(foods))
        f_part.write('\n'.join(parts))
        
        f_check.close()
        f_department.close()
        f_symptom.close()
        f_disease.close()
        f_food.close()
        f_part.close()

        return


#%%

if __name__ == '__main__':
    config = params()
    handler = MedicalGraph(config)
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")      
    handler.create_graphrels()    
    handler.export_data()
            
            
            
            
            
        
        
        
        
        
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        