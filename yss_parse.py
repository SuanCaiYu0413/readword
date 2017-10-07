# -*- coding: utf-8 -*-
# 验收书提取
from bs4 import BeautifulSoup


class yss():
    def __init__(self, html):

        self.soup = BeautifulSoup(html, "lxml")

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

    def parse(self):
        self.project_code()
        self.info_briefing()
        self.researchersr()
        return {'Researches': self.Researches, 'projectName': self.projectName, 'unitName': self.unitName,
                'projectCode': self.projectCode, 'infoBriefing': self.infoBriefing}

    '''
        项目编号
    '''

    def project_code(self):
        table = self.soup.find_all('table')[0]
        self.projectCode = table.find_all('tr')[0].find_all('td')[2].get_text().strip()
        self.projectName = table.find_all('tr')[1].find_all('td')[1].get_text().strip()
        self.unitName = table.find_all('tr')[2].find_all('td')[1].get_text().strip()

    '''
        信息简报
    '''

    def info_briefing(self):
        table = self.soup.find_all('table')[3]
        self.infoBriefing = table.find_all('tr')[1].get_text()

    '''
        人员解析
    '''

    def researchersr(self):
        table = self.soup.find_all('table')[5]
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
        r = yss(fp.read())
        fp.close()
        r.test()
