# -*- coding: utf-8 -*-
#验收书提取
from bs4 import BeautifulSoup

class yss():

    def __init__(self,html):

        self.soup = BeautifulSoup(html,"lxml")

        #项目编号
        self.projectCode = ''
        #信息简报
        self.infoBriefing = ''


    def parse(self):
        self.project_code()
        self.info_briefing()
        return {'projectCode':self.projectCode,'infoBriefing':self.infoBriefing}

    '''
        项目编号
    '''
    def project_code(self):
        table = self.soup.find_all('table')[0]
        self.projectCode = table.find_all('tr')[0].find_all('td')[2].get_text().strip()

    '''
        信息简报
    '''
    def info_briefing(self):
        table = self.soup.find_all('table')[3]
        self.infoBriefing = table.find_all('tr')[1].get_text()

    def test(self):
        tables = self.soup.find_all('table')
        print tables


if __name__ == "__main__":

    with open('./yss/10rkx0002yss.htm') as fp:
        r = yss(fp.read())
        fp.close()
        r.test()
