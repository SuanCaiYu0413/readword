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

        self.excel = None
        self.rws_dir = config.get('dir', 'rws')
        self.sbs_dir = config.get('dir', 'sbs')
        self.yss_dir = config.get('dir', 'yss')
        self.excel_dir = config.get('dir','result')
        self.create_file()

    def create_file(self):
        self.excel = xlwt.Workbook()
        self.yss_table = self.excel.add_sheet('yss', cell_overwrite_ok=True)
        self.rws_table = self.excel.add_sheet('rws', cell_overwrite_ok=True)
        self.rws_researchersr = self.excel.add_sheet('rws_researchersr', cell_overwrite_ok=True)
        self.rws_cooperationUnits = self.excel.add_sheet('rws_cooperationUnits', cell_overwrite_ok=True)
        self.sbs_table = self.excel.add_sheet('sbs', cell_overwrite_ok=True)
        self.sbs_researchersr = self.excel.add_sheet('sbs_researchersr', cell_overwrite_ok=True)
        self.sbs_cooperationUnits = self.excel.add_sheet('sbs_cooperationUnits', cell_overwrite_ok=True)

    def help(self):
        print u'run------------解析所有文档'
        print u'help----------帮助'
        print u'exit----------退出'

    def run(self):
        self.yss_parser()
        self.sbs_parser()
        self.rws_parser()

    def rws_parser(self):
        self.rws_table.write(0, 0, 'projectCode')
        self.rws_table.write(0, 1, 'researchareas')
        self.rws_table.write(0, 2, 'declareCode')
        l = ['name', 'degree', 'jobTitle', 'profession', 'declareCode']
        for index, name in enumerate(l):
            self.rws_researchersr.write(0, index, name)
        l = ['name', 'dtw', 'declareCode']
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
                    self.rws_table.write(index + 1, 0, rws_data['projectCode'])
                    self.rws_table.write(index + 1, 1, rws_data['researchareas'])
                    self.rws_table.write(index + 1, 2, rws_data['declareCode'])
                    for index1, item in enumerate(rws_data['researchersrs']):
                        l = ['name', 'degree', 'jobTitle', 'profession']
                        for i, str in enumerate(l):
                            self.rws_researchersr.write(index1 + 1, i, item[str])
                        self.rws_researchersr.write(index1 + 1, 4, rws_data['declareCode'])

                    for index2, item in enumerate(rws_data['cooperationUnits']):
                        l = ['name', 'dtw']
                        for i, str in enumerate(l):
                            self.rws_cooperationUnits.write(index2 + 1, i, item[str])
                        self.rws_cooperationUnits.write(index2 + 1, 2, rws_data['declareCode'])
                    print rws_data
                    self.excel.save(self.excel_dir)


    def sbs_parser(self):
        l1 = ['researchareas', 'declareCode', 'projectCode']
        for index, name in enumerate(l1):
            self.sbs_table.write(0, index, name)
        l2 = ['name', 'six', 'jobTitle', 'education', 'profession', 'declareCode']
        for index, name in enumerate(l2):
            self.sbs_researchersr.write(0, index, name)
        l3 = ['name', 'dtw', 'declareCode']
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
                    for index1, name in enumerate(l1):
                        self.sbs_table.write(index + 1, index1, sbs_data[name])
                    for index2, item in enumerate(sbs_data['researchersrs']):
                        l2 = ['name', 'six', 'jobTitle', 'education', 'profession']
                        for i, str in enumerate(l2):
                            self.sbs_researchersr.write(index2 + 1, i, item[str])
                        self.sbs_researchersr.write(index2 + 1, 5, sbs_data['declareCode'])
                    for index3, item in enumerate(sbs_data['cooperationUnits']):
                        l3 = ['name', 'dtw']
                        for i, str in enumerate(l3):
                            self.sbs_cooperationUnits.write(index3 + 1, i, item[str])
                        self.sbs_cooperationUnits.write(index3 + 1, 2, sbs_data['declareCode'])
                    print sbs_data
                    self.excel.save(self.excel_dir)

    def yss_parser(self):
        self.yss_table.write(0, 0, 'projectCode')
        self.yss_table.write(0, 1, 'infoBriefing')
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
                    self.yss_table.write(index + 1, 0, yss_data['projectCode'])
                    self.yss_table.write(index + 1, 1, yss_data['infoBriefing'])
            print yss_data
            self.excel.save(self.excel_dir)


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
            print '未知指令'
