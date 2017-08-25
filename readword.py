# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
with open(r'.\html\10rkx0002rws\10rkx0002rws.html') as fp:
    html = fp.read()
soup = BeautifulSoup(html,'lxml')
table =  soup.find_all('table')[9]
trs = table.find_all('tr')
qu = False
nameTrs = []
itea = False
its_tr = []
for tr in trs:
    if qu:
        nameTrs.append(tr)
    if tr.td.string != None and  tr.td.string.strip() == u'主要研究人员':
        qu = True


    if tr.td.string != None and  tr.td.string.strip() == u'项目负责人':
        itea = False
    if itea:
        its_tr.append(tr)
    if tr.td.string != None and  tr.td.string.strip() == u'协作单位':
        itea = True


for tr in nameTrs:
    tds = tr.find_all('td')
    if tds[0].get_text().strip() == "":
        continue
    print u'姓名:'+tds[0].get_text().strip()+'\t\t',
    print u'学位:'+tds[1].get_text().strip()+'\t\t',
    print u'职称:'+tds[2].get_text().strip()+'\t\t',
    print u'从事专业:'+tds[3].get_text().strip()

print '\n'

for tr in its_tr:
    tds = tr.find_all('td')
    if tds[0].get_text().strip() == "":
        continue
    print u'名称:' + tds[0].get_text().strip() + '\t\t',
    print u'分工:' + tds[1].get_text().strip()

print '\n'

table =  soup.find_all('table')[1]
print u'研究领域:' + table.find_all('tr')[2].get_text().split(u"：")[1]