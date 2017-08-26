# -*- coding: utf-8 -*-
import rws_parse
import sbs_parse
import yss_parse
with open(r'.\html\10rkx0002rws\10rkx0002rws.html') as fp:
    html = fp.read()
    fp.close()

rws = rws_parse.rws(html)
rws_data =  rws.parse()

print u'任务书解析'
print '------------------------------------------------'
print u'申报编号:',
print rws_data['declareCode']
print
print u'研究领域:',
print rws_data['researchareas']
print
print u'协助单位:'
print u'名称\t分工'
for item in rws_data['cooperationUnits']:
    print '%s\t%s'%(item['name'],item['dtw'])
print
print u'主要研究人员:'
print u'姓名\t学位\t职称\t专业'
for item in rws_data['researchersrs']:
    print '%s\t%s\t%s\t%s'%(item['name'],item['degree'],item['jobTitle'],item['profession'])
print '------------------------------------------------'

with open(r'.\html\10rkx0002sbs\10rkx0002sbs.html') as fp:
    html = fp.read()
    fp.close()
sbs = sbs_parse.sbs(html)

sbs_data = sbs.parse()

print u'申报书解析'
print '------------------------------------------------'
print u'申报编号:',
print sbs_data['declareCode']
print
print u'研究领域:',
print sbs_data['researchareas']
print
print u'协助单位:'
print u'名称\t分工'
for item in sbs_data['cooperationUnits']:
    print '%s\t%s'%(item['name'],item['dtw'])
print
print u'主要研究人员:'
print u'姓名\t性别\t职称\t学历\t专业'
for item in sbs_data['researchersrs']:
    print '%s\t%s\t%s\t%s\t%s'%(item['name'],item['six'],item['jobTitle'],item['education'],item['profession'])
print '------------------------------------------------'



with open(r'.\html\10rkx0002yss\10rkx0002yss.html') as fp:
    html = fp.read()
    fp.close()
yss = yss_parse.yss(html)

yss_data = yss.parse()

print u'验收书解析'
print '------------------------------------------------'
print u'项目编号:',
print yss_data['projectCode']
print
print u'信息简报:'
print yss_data['infoBriefing']
print '------------------------------------------------'
