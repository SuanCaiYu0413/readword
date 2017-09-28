# -*- coding: utf-8 -*-
#任务书内容提取
from bs4 import BeautifulSoup
import codecs
class rws():

    def __init__(self,html):
        self.soup = BeautifulSoup(html, 'lxml')
        #研究人员
        self.researchersrs = []
        #研究领域
        self.researchareas = ''
        #协作单位
        self.cooperationUnits = []
        #申报编号
        self.declareCode = ''
        #项目编号
        self.projectCode = ''
        #项目名称
        self.projectName = ''
        #第一负责单位
        self.oneUnit = {"name":"","unitNature":"","address":"","zipCode":""}
    '''
        总解析
    '''
    def parse(self):
        self.research_areas()
        self.researchersr()
        self.cooperation_units()
        self.declare_code()
        self.project_code()
        self.project_name()
        self.one_unit()
        return {'oneUnit':self.oneUnit,'projectName':self.projectName,'projectCode':self.projectCode,'researchersrs':self.researchersrs,'researchareas':self.researchareas,'cooperationUnits':self.cooperationUnits,'declareCode':self.declareCode}

    '''
        研究领域
    '''
    def research_areas(self):
        table = self.soup.find_all('table')[1]
        self.researchareas = table.find_all('tr')[2].get_text().split(u"：")[1]

    '''
        研究人员
    '''
    def researchersr(self):
        table = self.soup.find_all('table')[9]
        trs = table.find_all('tr')
        flag = False
        nameTrs = []
        for tr in trs:
            if flag:
                nameTrs.append(tr)
            if  tr.find_all('td')[0].get_text().strip() == u'主要研究人员':
                flag = True
        for tr in nameTrs:
            tds = tr.find_all('td')
            if tds[0].get_text().strip() == "":
                continue
            item = {}
            #姓名
            item['name'] = tds[0].get_text().strip()
            #学位
            item['degree'] = tds[1].get_text().strip()
            #职称
            item['jobTitle'] = tds[2].get_text().strip()
            #专业
            item['profession'] = tds[3].get_text().strip()
            self.researchersrs.append(item)

    '''
        协作单位
    '''
    def cooperation_units(self):
        table = self.soup.find_all('table')[9]
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
    def declare_code(self):
        table = self.soup.find_all('table')[0]
        self.declareCode = table.find_all('tr')[0].find_all('td')[1].get_text().strip()

    def project_code(self):
        table = self.soup.find_all('table')[0]
        self.projectCode = table.find_all('tr')[0].find_all('td')[3].get_text().strip()

    def test(self):
        tables = self.soup.find_all('table')
        print tables[9].find_all('tr')[0].get_text()

    def project_name(self):
        table = self.soup.find_all('table')[1]
        self.projectName = table.find_all('tr')[1].get_text().split(u"：")[1].strip()


    def one_unit(self):
        table = self.soup.find_all('table')[9]
        trs = table.find_all('tr')
        flag = False
        its_tr = []
        for tr in trs:
            if tr.find_all('td')[0].get_text().rstrip().replace("\n", "") == u'协作单位':
                flag = False
            if flag:
                its_tr.append(tr)
            if tr.find_all('td')[0].get_text().rstrip().replace("\n", "") == u'第一承担单位':
                its_tr.append(tr)
                flag = True
        self.oneUnit['name'] = its_tr[0].find_all('td')[2].get_text().strip()
        self.oneUnit['unitNature'] = its_tr[4].find_all('td')[3].get_text().strip()
        self.oneUnit['address'] = its_tr[1].find_all('td')[1].get_text().strip()
        self.oneUnit['zipCode'] = its_tr[1].find_all('td')[3].get_text().strip()

if __name__ == "__main__":


    with codecs.open(r'.\rws\10rkx0002rws.html','r','utf-16') as fp:
        r = rws(fp.read())
        r.one_unit()
