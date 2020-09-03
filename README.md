# Medical_KG
Medical Knowledge Graph 
the main structure and part of data are from https://github.com/liuhuanyong/QASystemOnMedicalKG

## 1.Intro 
The project mainly depends on the structure from https://github.com/liuhuanyong/QASystemOnMedicalKG. Apart from that, adding the drug recommend system on it and the drug data( original sql file) is from https://www.jiankangle.com/healthMall/category;jsessionid=FDC570E85A0BE68990B51FAB6307B454.

### Disease Data (2 types)


### Medicine Data


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


### CMD Results

## 3. Further Thoughts











