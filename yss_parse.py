# -*- coding: utf-8 -*-
# 验收书提取
from bs4 import BeautifulSoup

from log import Log


class yss():
    def __init__(self, html, filename):

        self.soup = BeautifulSoup(html, "lxml")

        self.keyword = {'info_table': [u'二、项目研究成果信息简报'],
                        'poples_table': [u'四、主要研究人员名单'],
                        'code_table': [u'项目编号', u'项目名称', u'起止年限']
                        }
        self.tables = {}
        self.filename = filename
        # 项目编号
        self.projectCode = ''
        # 信息简报
        self.infoBriefing = ''
        # 研究人员
        self.Researches = []
        # 项目名称
        self.projectName = ''
        # 单位名称
        self.unitName = ''
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
        if 'code_table' in self.tables:
            self.project_code(self.tables['code_table'])
        else:
            Log.write(u'%s:未找到文档信息表格' % self.filename)
        if 'poples_table' in self.tables:
            self.researchersr(self.tables['poples_table'])
        else:
            Log.write(u'%s:未找到人员信息表格' % self.filename)
        if 'info_table' in self.tables:
            self.info_briefing(self.tables['info_table'])
        else:
            Log.write(u'%s:未找到信息简报表格' % self.filename)

        return {'Researches': self.Researches, 'projectName': self.projectName, 'unitName': self.unitName,
                'projectCode': self.projectCode, 'infoBriefing': self.infoBriefing}

    '''
        项目编号
    '''

    def project_code(self, table):

        self.projectCode = table.find_all('tr')[0].find_all('td')[2].get_text().strip()
        self.projectName = table.find_all('tr')[1].find_all('td')[1].get_text().strip()
        self.unitName = table.find_all('tr')[2].find_all('td')[1].get_text().strip()

    '''
        信息简报
    '''

    def info_briefing(self, table):

        self.infoBriefing = table.find_all('tr')[1].get_text()

    '''
        人员解析
    '''

    def researchersr(self, table):

        trs = table.find_all('tr')[2:]
        for tr in trs:
            people = {}
            if tr.find_all('td')[0].get_text().strip() != "":
                people['name'] = tr.find_all('td')[0].get_text().strip()
                people['age'] = tr.find_all('td')[1].get_text().strip()
                people['education'] = tr.find_all('td')[2].get_text().strip()
                people['profession'] = tr.find_all('td')[3].get_text().strip()
                people['jobTitle'] = tr.find_all('td')[4].get_text().strip()
                people['jobUnit'] = tr.find_all('td')[5].get_text().strip()
                people['contribution'] = tr.find_all('td')[6].get_text().strip()
                self.Researches.append(people)

    def test(self):
        pass


if __name__ == "__main__":
    with open('./yss/10rkx0002yss.htm') as fp:
        r = yss(fp.read(), 'adasd')
        fp.close()
        print len(r.tables)
