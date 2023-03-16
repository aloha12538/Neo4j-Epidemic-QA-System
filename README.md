# Neo4j-Epidemic-QA-System
Epidemic Q&amp;A System

##数据来源
北京市疫情数据，因为涉及隐私，暂不提供

## 运行环境
Windows系统
python==3.9
py2neo==2021.2.3
java JDK==8
neo4j==community-3.5.32-windows

## 运行步骤
1.	将csv数据导入neo4j
在“实验数据”目录下，将“北京疫情人员统计.csv”、“关系表.csv”文件放在<NEO4J_HOME\import>目录下，启动neo4j，在浏览器中打开页面，http://localhost:7474/，在窗口依次运行以下命令，完成数据导入。
LOAD CSV WITH HEADERS  FROM "file:///person_Format.csv" AS line
MERGE (p:person{id:line.id,name:line.name,age:line.age})

LOAD CSV WITH HEADERS FROM "file:///北京疫情人员统计.csv" As line 
MERGE (p:CaseBeijing {Date:line["日期"],Region:line["地区"],Number:line["编号"],CaseSource:line["病例来源"],Address:line["地址"],Profession:line["职业"]})

LOAD CSV WITH HEADERS FROM "file:///关系表.csv" As line
MATCH (from:CaseBeijing{Number:line["对象1"]}),(to:CaseBeijing{Number:line["对象2"]})
MERGE (from)-[r:Relation{RelationshipType:line["关系类型"]}]->(to)

START n=node(*) RETURN n

2.	运行py程序完成知识问答
在pycharm或anaconda中配置好运行环境及相关依赖库后，将data文件夹、test.py、template_method.py放置在同一目录下，运行test.py，即可完成知识问答。
在test.py文件中，修改第14行question对象的内容，即可完成不同问题的问答，其中问题的模板在date/question_template.txt文件中。

## 文件结构说明
“实验数据”文件夹：存放“北京疫情人员统计.csv”和“关系表.csv”文件，用于导入neo4j数据库。
“date”文件夹：存放python程序运行时所需的txt数据，用于关键字匹配和模板匹配。“CaseSource.txt”存放病例来源关键字，“Date.txt”存放日期关键字，“InfectedPerson.txt”存放感染者编号，“Profession.txt”存放职业关键字，“Region.txt”存放地区关键字，“Relatinship.txt”存放关系关键字，“question_template.txt”存放问题模板。
test.py：程序运行主文件。
template_method.py：新建类文件。

