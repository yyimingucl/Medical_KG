# Medical_KG
Medical Knowledge Graph 
the main structure and part of data are from https://github.com/liuhuanyong/QASystemOnMedicalKG

## 1.Intro 

The project mainly depends on the structure from https://github.com/liuhuanyong/QASystemOnMedicalKG. Apart from that, adding the drug recommend system on it and the drug data  is from https://www.jiankangle.com/healthMall/category;jsessionid=FDC570E85A0BE68990B51FAB6307B454.

### Disease Data (2 types)
![image](https://raw.githubusercontent.com/MissuQAQ/Medical_KG/master/image_file/1599125227(1).png)

![image](https://raw.githubusercontent.com/MissuQAQ/Medical_KG/master/image_file/1599125801(1).png)
### Medicine Data
![image](https://github.com/MissuQAQ/Medical_KG/blob/master/image_file/1599125871(1).png)

KG_data.py: match the disease and medicine (but the result is not so good)
KG_parameters.py: store the various paths of data
KG_functions.py: store some used functions in this project
build_graph.py: upload the structured data to neo4j database
classifier: classify the intention of the patient's query
paser.py: transfer to required sql query sentence
searcher.py: return the information queried
drug_recommend.py: return the recommended drug


## 2.Knowledge Graph

It contains 9 kinds of nodes (category of drug, drug, disease,symptom, food, department, check, parts) and 12 kinds of relationships
Totally 28000 entity nodes and 360000 relationships

### Neo4j DataBase
![image](https://raw.githubusercontent.com/MissuQAQ/Medical_KG/master/image_file/1599126788(1).png)

### Command Line Results
![image](https://raw.githubusercontent.com/MissuQAQ/Medical_KG/master/image_file/1599193907(1).png)



## 3.Further Thoughts
the main method to classify question and name entity is based on string matching which is highly dependent on the size of vocabulary and not flexible. 

Further Suggestion:
1. Using a NER model like BiLSTM+CRF, HMM and some other sequential models extracts the entities which could be applied to much more cases and avoid the limition of the vocabulary size.
2. Applying a method that compare the similarity of words and transfer the entity extracted from NER model to standard key words in SQL. Carry out the sql query and return the required answer. 













