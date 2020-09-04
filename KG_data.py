# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 02:01:13 2020

@author: yyimi

Process Data 
"""
import re, pymysql
import pandas as pd
from KG_parameters import params 
from KG_functions import AC_Automaton
config = params()



#%%
def load_disease_data(path): 
    data = pd.read_csv(path)
    data = data.fillna(-1)
    print('------------------Loading Disease Data--------------------------')
    return data
            

def load_medicine_data():
    '''
    load medicine data from database
    -------
    pd.Dataframe
    '''
    db = pymysql.connect("127.0.0.1", "root", "YYMabc990906",
                         "medicine", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM medicine_data")
    cols = cursor.description
    Dataset_Q = cursor.fetchall()
    cursor.close()
    db.close()
    column_names = [col[0] for col in cols]
    data = pd.DataFrame(Dataset_Q)
    data = data.fillna(-1)
    data.columns = column_names
    data = data.drop(index = 
                     data[data.prescription_type == '非药品'].index)
    
    print('------------------Loading Drug Data--------------------------')
    
    return data


#%%
def match_data(med_data, dis_data):
    '''
    
    Parameters
    ----------
    med_data : pd.DataFrame (medicine data)
    dis_data : pd.DataFrame (disease data)
    
    Returns
    -------
    dict
    try to find the relation between medicine and disease
    {disease : medicine}
    '''
    pattern = u'[^\u4e00-\u9fa5_a-zA-Z]'
    regex = re.compile(pattern)
    
    
    #1.Match relation from drug info in disease data
    tmp = [] # shore the corresponding drug from disease data
    relation = []
    
    for i,(dis_name, drug_names) in enumerate(zip(dis_data.name, dis_data.drug)):
        #print(drug_name)
        if (type(drug_names) == str) and (drug_names != '>> 应该如何用药？用什么药？ [详细]'):
            drug_name = [regex.sub('',each).strip() for each in drug_names.split()[:-1]]
            #avoid duplicat check
            dis_data.drop([i],axis = 0,inplace = False) 
        else:
            drug_name = []
        tmp.append((drug_name,dis_name))
        
        
    for goods in med_data.goods_name:
        #goods_name longer than common name (ie should contain the common name)
        g_name = regex.sub('', goods).strip()
        for short_name in tmp:
            for each in short_name[0]:
                if each in g_name:
                    relation.append((short_name[1], goods))
    
        
    
    #2. disease name and indication from drug instruction
    name = dis_data.name.tolist()
    used_meddata = med_data[(med_data.indication!=-1)&(med_data.indication!='')][['goods_name','indication']]
    indication = used_meddata.indication.tolist()
    drug_name_set = used_meddata.goods_name.tolist()
    
    disease_tree = AC_Automaton(name)
    for drug_name, ind in zip(drug_name_set, indication):
        cor_dis = disease_tree.match_medical(ind)
        for each in cor_dis:
            relation.append((each,drug_name.strip()))
    
    
    
    #3. match from symptom and indication
    used_disdata = dis_data[(dis_data.symptom!=-1)&(dis_data.symptom!='')][['name','symptom']]
    name = used_disdata.name.tolist()
    symptom_set = used_disdata.symptom.tolist()
    
    for dis_name, dis_symptom in zip(name, symptom_set):
        if type(dis_symptom) == str:
            symptom = [regex.sub('',each).strip() for each in dis_symptom.split()[:-1]]
            if symptom != []:
                sym_tree = AC_Automaton(symptom)
                for ind, drug_name in zip(indication, drug_name_set):
                    if len(sym_tree.match_medical(ind)) >= 4:
                        relation.append((dis_name, drug_name.strip()))
            
    dict_res = {dis : [] for dis in dis_data.name}
    for each in list(set(relation)):
        dict_res[each[0]].append(each[1])
    
    return dict_res 



#%%
if __name__ == '__main__':
    relation = match_data(load_medicine_data(), load_disease_data(config.disease_data))
    with open(config.relation_path, mode = 'w', encoding = 'utf-8') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in relation.items()]
    f.close()

    






