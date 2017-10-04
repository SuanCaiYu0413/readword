# -*- coding: utf-8 -*-
#html文档内容提取
import ConfigParser
import rws_parse
import sbs_parse
import yss_parse
import os
import xlwt
import codecs

class DataParser():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        with open('./config.ini', 'rb') as fp:
            config.readfp(fp)

        self.excel_rws = None
        self.excel_sbs = None
        self.excel_yss = None
        self.rws_dir = config.get('dir', 'rws')
        self.sbs_dir = config.get('dir', 'sbs')
        self.yss_dir = config.get('dir', 'yss')
        self.excel_dir = config.get('dir','result')
        self.excel_dir = [self.excel_dir + i + '.xls' for i in '123']
        print self.excel_dir
        self.create_file()

    def create_file(self):
        self.excel_rws = xlwt.Workbook()
        self.excel_sbs = xlwt.Workbook()
        self.excel_yss = xlwt.Workbook()
        self.yss_table = self.excel_yss.add_sheet(u'验收书', cell_overwrite_ok=True)
        self.yss_researchersr = self.excel_yss.add_sheet(u'研究人员', cell_overwrite_ok=True)
        self.rws_table = self.excel_rws.add_sheet(u'任务书', cell_overwrite_ok=True)
        self.rws_researchersr = self.excel_rws.add_sheet(u'研究人员', cell_overwrite_ok=True)
        self.rws_cooperationUnits = self.excel_rws.add_sheet(u'协作单位', cell_overwrite_ok=True)
        self.sbs_table = self.excel_sbs.add_sheet(u'申报书', cell_overwrite_ok=True)
        self.sbs_researchersr = self.excel_sbs.add_sheet(u'研究人员', cell_overwrite_ok=True)
        self.sbs_cooperationUnits = self.excel_sbs.add_sheet(u'协作单位', cell_overwrite_ok=True)

    def help(self):
        print u'run------------解析所有文档'
        print u'help----------帮助'
        print u'exit----------退出'

    def run(self):
        self.yss_parser()
        self.sbs_parser()
        self.rws_parser()

    def rws_parser(self):
        rowNo = {"rws":1,"researchersr":1,"cooperationUnits":1}

        self.rws_table.write(0, 0, u'计划编号')
        self.rws_table.write(0, 1, u'研究领域')
        self.rws_table.write(0, 2, u'申报编号')
        self.rws_table.write(0, 3, u'项目名称')

        l = [u'序号',u'姓名', u'学位', u'职称', u'专业', u'申报编号']
        for index, name in enumerate(l):
            self.rws_researchersr.write(0, index, name)
        l = [u'序号',u'名称', u'分工', u'申报编号',u'单位性质',u'地址',u'邮编']
        for index, name in enumerate(l):
            self.rws_cooperationUnits.write(0, index, name)
        for index, file in enumerate(os.listdir(self.rws_dir)):
            filename = os.path.join(self.rws_dir, file)
            if os.path.isfile(filename):
                if os.path.splitext(filename)[1].strip() == '.html':
                    with codecs.open(filename,'r','utf-16') as fp:
                        html = fp.read()
                        fp.close()
                if os.path.splitext(filename)[1].strip() == '.htm':
                    with open(filename) as fp:
                        html = fp.read()
                        fp.close()
                if html:
                    rws_data = rws_parse.rws(html).parse()
                    self.rws_table.write(rowNo['rws'], 0, rws_data['projectCode'])
                    self.rws_table.write(rowNo['rws'], 1, rws_data['researchareas'])
                    self.rws_table.write(rowNo['rws'], 2, rws_data['declareCode'])
                    self.rws_table.write(rowNo['rws'], 3, rws_data['projectName'])
                    rowNo['rws'] += 1
                    for index1, item in enumerate(rws_data['researchersrs']):
                        l = ['name', 'degree', 'jobTitle', 'profession']
                        self.rws_researchersr.write(rowNo['researchersr'], 0, index1+1)
                        for i, str in enumerate(l):
                            self.rws_researchersr.write(rowNo['researchersr'], i+1, item[str])
                        self.rws_researchersr.write(rowNo['researchersr'], 5, rws_data['declareCode'])
                        rowNo['researchersr'] += 1
                    self.rws_cooperationUnits.write(rowNo['cooperationUnits'], 0, 1)
                    self.rws_cooperationUnits.write(rowNo['cooperationUnits'], 1, rws_data['oneUnit']['name'])
                    self.rws_cooperationUnits.write(rowNo['cooperationUnits'], 3, rws_data['declareCode'])
                    self.rws_cooperationUnits.write(rowNo['cooperationUnits'], 4, rws_data['oneUnit']['unitNature'])
                    self.rws_cooperationUnits.write(rowNo['cooperationUnits'], 5, rws_data['oneUnit']['address'])
                    self.rws_cooperationUnits.write(rowNo['cooperationUnits'], 6, rws_data['oneUnit']['zipCode'])
                    rowNo['cooperationUnits'] += 1
                    for index2, item in enumerate(rws_data['cooperationUnits']):
                        l = ['name', 'dtw']
                        self.rws_cooperationUnits.write(rowNo['cooperationUnits'], 0, index2+2)
                        for i, str in enumerate(l):
                            self.rws_cooperationUnits.write(rowNo['cooperationUnits'], i+1, item[str])
                        self.rws_cooperationUnits.write(rowNo['cooperationUnits'], 3, rws_data['declareCode'])
                    rowNo['cooperationUnits'] += 1
                    print file
                self.excel_rws.save(self.excel_dir[0])


    def sbs_parser(self):
        rowNo = {"sbs":1,"researchersr":1,"cooperationUnits":1}
        l1 = [u'计划编号',u'研究领域', u'申报编号',  u'项目名称']
        for index, name in enumerate(l1):
            self.sbs_table.write(0, index, name)
        l2 = [u'序号',u'姓名', u'性别', u'职称', u'学历', u'专业', u'申报编号']
        for index, name in enumerate(l2):
            self.sbs_researchersr.write(0, index, name)
        l3 = [u'序号',u'名称', u'分工', u'申报编号',u'单位性质',u'地址',u'邮编']
        for index, name in enumerate(l3):
            self.sbs_cooperationUnits.write(0, index, name)
        for index, file in enumerate(os.listdir(self.sbs_dir)):
            filename = os.path.join(self.sbs_dir, file)
            if os.path.isfile(filename):
                if os.path.splitext(filename)[1].strip() == '.html':
                    with codecs.open(filename,'r','utf-16') as fp:
                        html = fp.read()
                        fp.close()
                if os.path.splitext(filename)[1].strip() == '.htm':
                    with open(filename) as fp:
                        html = fp.read()
                        fp.close()
                if html:
                    sbs_data = sbs_parse.sbs(html).parse()
                    l1 = [ 'projectCode','researchareas','declareCode','projectName']
                    for index1, name in enumerate(l1):
                        self.sbs_table.write(rowNo['sbs'], index1, sbs_data[name])
                    rowNo['sbs'] += 1
                    for index2, item in enumerate(sbs_data['researchersrs']):
                        l2 = ['name', 'six', 'jobTitle', 'education', 'profession']
                        self.sbs_researchersr.write(rowNo['researchersr'], 0, index2+1)
                        for i, str in enumerate(l2):
                            self.sbs_researchersr.write(rowNo['researchersr'], i+1, item[str])
                        self.sbs_researchersr.write(rowNo['researchersr'], 6, sbs_data['declareCode'])
                        rowNo['researchersr'] += 1

                    self.sbs_cooperationUnits.write(rowNo['cooperationUnits'], 0, 1)
                    self.sbs_cooperationUnits.write(rowNo['cooperationUnits'], 1, sbs_data['oneUnit']['name'])
                    self.sbs_cooperationUnits.write(rowNo['cooperationUnits'], 3, sbs_data['declareCode'])
                    self.sbs_cooperationUnits.write(rowNo['cooperationUnits'], 4, sbs_data['oneUnit']['unitNature'])
                    self.sbs_cooperationUnits.write(rowNo['cooperationUnits'], 5, sbs_data['oneUnit']['address'])
                    self.sbs_cooperationUnits.write(rowNo['cooperationUnits'], 6, sbs_data['oneUnit']['zipCode'])
                    rowNo['cooperationUnits'] += 1
                    for index3, item in enumerate(sbs_data['cooperationUnits']):
                        l3 = ['name', 'dtw']
                        self.sbs_cooperationUnits.write(rowNo['cooperationUnits'], 0, index3+2)
                        for i, str in enumerate(l3):
                            self.sbs_cooperationUnits.write(rowNo['cooperationUnits'], i+1, item[str])
                        self.sbs_cooperationUnits.write(rowNo['cooperationUnits'], 3, sbs_data['declareCode'])
                        rowNo['cooperationUnits'] += 1
                    print file
                    self.excel_sbs.save(self.excel_dir[1])

    def yss_parser(self):
        rowNo = {'yss':1,'researchersr':1}
        self.yss_table.write(0, 0, u'计划编号')
        self.yss_table.write(0, 1, u'成果信息简报')
        self.yss_table.write(0, 2, u'项目名称')
        self.yss_table.write(0, 3, u'单位名称')
        li = [u'姓名',u'年龄',u'文化程度',u'所学专业',u'职务职称',u'工作单位',u'贡献',u'计划编号']
        for index,item in enumerate(li):
            self.yss_researchersr.write(0,index,item)
        for index, file in enumerate(os.listdir(self.yss_dir)):
            filename = os.path.join(self.yss_dir, file)
            if os.path.isfile(filename):
                if os.path.splitext(filename)[1].strip() == '.html':
                    with codecs.open(filename,'r','utf-16') as fp:
                        html = fp.read()
                        fp.close()
                if os.path.splitext(filename)[1].strip() == '.htm':
                    with open(filename) as fp:
                        html = fp.read()
                        fp.close()
                if html:
                    yss_data = yss_parse.yss(html).parse()
                    self.yss_table.write(rowNo['yss'], 0, yss_data['projectCode'])
                    self.yss_table.write(rowNo['yss'], 1, yss_data['infoBriefing'])
                    self.yss_table.write(rowNo['yss'], 2, yss_data['projectName'])
                    self.yss_table.write(rowNo['yss'], 3, yss_data['unitName'])
                    rowNo['yss'] += 1

                    for index1,item in enumerate(yss_data['Researches']):
                        li = ['name','age','education','profession','jobTitle','jobUnit','contribution']
                        self.yss_researchersr.write(rowNo['researchersr'], 0, index1+1)
                        for ix,data in enumerate(li):
                            self.yss_researchersr.write(rowNo['researchersr'],ix+1,item[li[ix]])
                        self.yss_researchersr.write(rowNo['researchersr'],8, yss_data['projectCode'])
                        rowNo['researchersr'] += 1

            print file
            self.excel_yss.save(self.excel_dir[2])


if __name__ == "__main__":
    dp = DataParser()
    dp.help()
    while True:
        input = raw_input('>>')
        if input == 'help':
            dp.help()
        elif input == 'exit':
            exit(1)
        elif input == 'run':
            dp.run()
        else:
            print u'未知指令'