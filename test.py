import re
import sys

from py2neo import Graph
from template_method import TempMethod

#链接neo4j图谱
graph = Graph("http://localhost:7474",auth=("neo4j", "m18406596008") )

#加载问题模板
c = TempMethod(graph, 'data/question_template.txt')

#本次的问题
question = '感染者164与多少个感染者有关系'
print("提问：\n%s\n"%(question))
#判断问题的大类
question_type = c.match(question)
# match函数用来获取问题类别
print("类别:\n%s\n"%(question_type))
#根据问题进行关键词提取，并生成答案
query_res_list = c.generate_answer(question_type, question)
# generate_answer函数用来生成答案
print()
#打印答案
print("答案：")
for query_res in query_res_list:
            print(query_res)