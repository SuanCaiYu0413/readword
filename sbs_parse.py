# -*- coding: utf-8 -*-
# 申报书内容提取
import codecs
from log import Log
from bs4 import BeautifulSoup


class sbs():
    def __init__(self, html, filename):
        self.soup = BeautifulSoup(html, 'lxml')

        self.keyword = {'baseinfo_table': [u'承担单位', u'现从事专业', u'在本项目中的分工', u'归口部门'],
                        'field_table': [u'研究领域', u'立项的必要性及国内外研究现状', u'项目名称'],
                        'code_table': [u'申报编号', u'计划编号', u'密级']
                        }
        self.tables = {}
        self.filename = filename
        # 研究人员
        self.researchersrs = []
        # 研究领域
        self.researchareas = ''
        # 协作单位
        self.cooperationUnits = []
        # 申报编号
        self.declareCode = ''
        # 项目编号
        self.projectCode = ''
        # 项目名称
        self.projectName = ''
        # 第一负责单位
        self.oneUnit = {"name": "", "unitNature": "", "address": "", "zipCode": ""}
        self.find()

    def find(self):
        tables = self.soup.find_all('table')
        for table in tables:
            string = table.get_text().strip().replace('\n', '').replace(' ', '')
            for key in self.keyword:
                count = 0
                for keyword in self.keyword[key]:
                    if string.find(keyword) != -1:
                        count += 1
                if count == len(self.keyword[key]):
                    self.tables[key] = table

    def parse(self):

        if 'baseinfo_table' in self.tables:
            self.one_unit(self.tables['baseinfo_table'])
            self.cooperation_units(self.tables['baseinfo_table'])
            self.researchersr(self.tables['baseinfo_table'])
        else:
            Log.write(u'%s:为查找到人员信息表格' % self.filename)

        if 'code_table' in self.tables:
            self.declare_code(self.tables['code_table'])
            self.project_code(self.tables['code_table'])
        else:
            Log.write(u'%s:为查找到文档信息表格' % self.filename)

        if 'field_table' in self.tables:
            self.research_areas(self.tables['field_table'])
            self.project_name(self.tables['field_table'])
        else:
            Log.write(u'%s:为查找到研究领域信息表格' % self.filename)

        return {'oneUnit': self.oneUnit, 'projectName': self.projectName, 'projectCode': self.projectCode,
                'researchersrs': self.researchersrs, 'researchareas': self.researchareas,
                'cooperationUnits': self.cooperationUnits, 'declareCode': self.declareCode}

    '''
        研究领域
    '''

    def research_areas(self, table):

        self.researchareas = table.find_all('tr')[1].find_all('td')[1].get_text()

    '''
        项目名称
    '''

    def project_name(self, table):
        self.projectName = table.find_all('tr')[0].find_all('td')[1].get_text().strip()

    '''
        研究人员
    '''

    def researchersr(self, table):
        trs = table.find_all('tr')
        flag = False
        its_tr = []
        for tr in trs:
            if tr.find_all('td')[0].get_text().strip() == u'项目组人数':
                flag = False
            if flag:
                its_tr.append(tr)
            if tr.find_all('td')[0].get_text().strip() == u'项目负责人':
                its_tr.append(tr)
                flag = True
        item_zhu = {}
        # 姓名
        item_zhu['name'] = its_tr[0].find_all('td')[2].get_text().strip()
        # 性别
        item_zhu['six'] = its_tr[0].find_all('td')[4].get_text().strip()
        # 职称
        item_zhu['jobTitle'] = its_tr[1].find_all('td')[1].get_text().strip()
        # 学历
        item_zhu['education'] = its_tr[0].find_all('td')[8].get_text().strip()
        # 专业
        item_zhu['profession'] = its_tr[1].find_all('td')[5].get_text().strip()
        self.researchersrs.append(item_zhu)

        flag = False
        nameTrs = []
        for tr in trs:
            if tr.find_all('td')[0].get_text().strip() == u'归口部门意见':
                flag = False
            if flag:
                nameTrs.append(tr)
            if tr.find_all('td')[0].get_text().strip() == u'主要研究人员':
                flag = True

        for tr in nameTrs:
            tds = tr.find_all('td')
            if tds[0].get_text().strip() == "":
                continue
            item = {}
            # 姓名
            item['name'] = tds[0].get_text().strip()
            # 性别
            item['six'] = tds[1].get_text().strip()
            # 职称
            item['jobTitle'] = tds[2].get_text().strip()
            # 学历
            item['education'] = tds[3].get_text().strip()
            # 专业
            item['profession'] = tds[4].get_text().strip()
            if item['name'] != item_zhu['name']:
                self.researchersrs.append(item)

    '''
        协作单位
    '''

    def cooperation_units(self, table):
        trs = table.find_all('tr')
        flag = False
        its_tr = []
        for tr in trs:
            if tr.find_all('td')[0].get_text().strip() == u'项目负责人':
                flag = False
            if flag:
                its_tr.append(tr)
            if tr.find_all('td')[0].get_text().strip() == u'协作单位':
                flag = True

        for tr in its_tr:
            tds = tr.find_all('td')
            if tds[0].get_text().strip() == "":
                continue
            item = {}
            # 名称
            item['name'] = tds[0].get_text().strip()
            # 分工
            item['dtw'] = tds[1].get_text().strip()
            self.cooperationUnits.append(item)

    '''
        申报编号
    '''

    def declare_code(self, table):

        self.declareCode = table.find_all('tr')[0].find_all('td')[1].get_text().strip()

    def project_code(self, table):

        self.projectCode = table.find_all('tr')[0].find_all('td')[3].get_text().strip()

    def one_unit(self, table):

        trs = table.find_all('tr')
        flag = False
        its_tr = []
        for tr in trs:
            if tr.find_all('td')[0].get_text().strip() == u'协作单位':
                flag = False
            if flag:
                its_tr.append(tr)
            if tr.find_all('td')[0].get_text().strip() == u'承担单位':
                its_tr.append(tr)
                flag = True
        self.oneUnit['name'] = its_tr[0].find_all('td')[2].get_text().strip()
        self.oneUnit['unitNature'] = its_tr[2].find_all('td')[3].get_text().strip()
        self.oneUnit['address'] = its_tr[1].find_all('td')[1].get_text().strip()
        self.oneUnit['zipCode'] = its_tr[1].find_all('td')[3].get_text().strip()


if __name__ == "__main__":
    with codecs.open(r'.\sbs\10RKX0066sbs.html', 'r', 'utf-16') as fp:
        r = sbs(fp.read(), 'asd')
        print r.parse()
