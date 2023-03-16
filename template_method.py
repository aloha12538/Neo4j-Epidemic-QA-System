import re
import sys
import collections


class TempMethod:
    def __init__(self, graph, template_path):
        self.casesource = self.load_word_list('data/CaseSource.txt')
        self.date = self.load_word_list('data/Date.txt')
        self.infectedperson = self.load_word_list('data/InfectedPerson.txt')
        self.profession = self.load_word_list('data/Profession.txt')
        self.region = self.load_word_list('data/Region.txt')
        self.relationship = self.load_word_list('data/Relationship.txt')
        casesource_str = '|'.join(self.casesource)
        date_str = '|'.join(self.date)
        infectedperson_str = '|'.join(self.infectedperson)
        profession_str = '|'.join(self.profession)
        region_str = '|'.join(self.region)
        relationship_str = '|'.join(self.relationship)
        self.r_casesource = re.compile(r"(%s)" % (casesource_str))
        self.r_date = re.compile(r"(%s)" % (date_str))
        self.r_infectedperson = re.compile(r"(%s)" % (infectedperson_str))
        self.r_profession = re.compile(r"(%s)" % (profession_str))
        self.r_region = re.compile(r"(%s)" % (region_str))
        self.r_relationship = re.compile(r"(%s)" % (relationship_str))
        self.template_dict = {}
        self.graph = graph
        self.word_del = re.compile(r'(xx月xx日的|xx月|xx区|感染者xx和感染者xx|感染者xx|xx感染者|xx病例|xx职)')
        with open(template_path, encoding='utf8') as f:
            temp_label = ''
            for line in f:
                if not line.strip():
                    continue
                if line.strip().startswith('#'):
                    temp_label = line.strip()[1:]
                    self.template_dict[temp_label] = []
                else:
                    self.template_dict[temp_label].append(line.strip())
        return

    def load_word_list(self, path):
        temp_list = []
        with open(path, encoding='utf8') as f:
            for line in f:
                temp_list.append(line.strip())
        return temp_list

    def match(self, question):
        for key, val in self.template_dict.items():
            for template in val:
                real_temp = self.word_del.sub('', template)
                if question.find(real_temp) >= 0:
                    return key

    def relation_query(self, key, question_type, type):
        query_res = ''
        if type == 0:
            query_res = self.graph.run('MATCH (n:CaseBeijing {%s:"%s"}) return COUNT(n) AS COUNT' % (question_type, key))
            query_res = str(query_res.data()).strip("[{'COUNT': ").strip(")}]")
        if type == 1:
            query_res = self.graph.run('MATCH (n:CaseBeijing {%s:"%s"}) return n' % (question_type, key))
            query_res = str(query_res.data()).strip("[{'n': Node('CaseBeijing', ").strip(")}]")
        if type == 2:
            query_res = self.graph.run('MATCH (n:CaseBeijing {%s:"%s"}) return n.Region' % (question_type, key))
            query_res = str(query_res.data()).strip("[{'n.Region': ").strip("'}]")
        if type == 3:
            query_res = self.graph.run('MATCH (n:CaseBeijing {%s:"%s"}) return n.Profession' % (question_type, key))
            query_res = str(query_res.data()).strip("[{'n.Profession': ").strip("'}]")
        if type == 4:
            query_res = self.graph.run('MATCH (n:CaseBeijing {%s:"%s"}) return n.CaseSource' % (question_type, key))
            query_res = str(query_res.data()).strip("[{'n.CaseSource': ").strip("'}]")
        if type == 5:
            number1 = key[0]
            number2 = key[1]
            query_res = self.graph.run(
                "MATCH (n:CaseBeijing {Number:'%s'})-[r:Relation]->(m:CaseBeijing {Number:'%s'}) return r" % (number1, number2))
            query_res = str(query_res.data()).strip("')}]")
            pos = re.search("Type='", query_res).span()
            a = pos[1]
            query_res = query_res[a:]
        if type == 6:
            number = key[0]
            #query_res = self.graph.run("MATCH q = (n:CaseBeijing {Number:'%s'})-[*1..2]-() return q" % (number))
            query_res = self.graph.run("MATCH q = (n:CaseBeijing {Number:'%s'})-[*1..2]-() return q" % (number))
            query_res = str(query_res.data())
            pos = re.findall("Path", query_res)
            query_res = len(pos)
        return query_res


    def generate_answer(self, question_type, question):
        query_res_list = []
        casesource_list = self.r_casesource.findall(question)
        date_list = self.r_date.findall(question)
        infectedperson_list = self.r_infectedperson.findall(question)
        profession_list = self.r_profession.findall(question)
        region_list = self.r_region.findall(question)
        relationship_list = self.r_relationship.findall(question)
        print("关键词提取:")
        if casesource_list:
            print(casesource_list)
        if date_list:
            print(date_list)
        if infectedperson_list:
            print(infectedperson_list)
        if profession_list:
            print(profession_list)
        if region_list:
            print(region_list)
        if relationship_list:
            print(relationship_list)

        if question_type == 'Date':
            if date_list:
                for item in date_list:
                    query_res = self.relation_query(item, question_type, type=0)
                    query_res_list.append(query_res)
            elif date_list == []:
                if question.find('4') >= 0:
                    date_list = ['4月22日', '4月23日', '4月24日', '4月25日', '4月26日', '4月27日', '4月28日', '4月29日', '4月30日']
                if question.find('5') >= 0:
                    date_list = ["5月1日"]
                for item in date_list:
                    query_res = self.relation_query(item, question_type, type=0)
                    query_res_list.append(query_res)
                    res = 0
                    for ele in range(0, len(query_res_list)):
                        res += int(query_res_list[ele])
                    query_res_list = [str(res)]

        if question_type == 'Region':
            if region_list:
                for item in region_list:
                    query_res = self.relation_query(item, question_type, type=0)
                    query_res_list.append(query_res)

        if question_type == 'Relationship':
            if len(infectedperson_list) == 2:
                query_res = self.relation_query(infectedperson_list, question_type, type=5)
                query_res_list.append(query_res)
            if len(infectedperson_list) == 1:
                query_res = self.relation_query(infectedperson_list, question_type, type=6)
                query_res_list.append(query_res)

        if question_type == 'Number':
            if question.find('详细信息')>=0:
                for item in infectedperson_list:
                    query_res = self.relation_query(item, question_type, type=1)
                    query_res_list.append(query_res)
            if question.find('地区')>=0:
                for item in infectedperson_list:
                    query_res = self.relation_query(item, question_type, type=2)
                    query_res_list.append(query_res)
            if question.find('职业')>=0:
                for item in infectedperson_list:
                    query_res = self.relation_query(item, question_type, type=3)
                    query_res_list.append(query_res)
            if question.find('病例来源')>=0:
                for item in infectedperson_list:
                    query_res = self.relation_query(item, question_type, type=4)
                    query_res_list.append(query_res)

        if question_type == 'Profession':
            if profession_list:
                for item in profession_list:
                    query_res = self.relation_query(item, question_type, type=0)
                    query_res_list.append(query_res)

        if question_type == 'CaseSource':
            if casesource_list:
                for item in casesource_list:
                    query_res = self.relation_query(item, question_type, type=0)
                    query_res_list.append(query_res)

        return query_res_list