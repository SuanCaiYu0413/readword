# -*- coding: utf-8 -*-
#word文档转html文档
from win32com import  client as wc
# import codecs
import os
wordDir = os.getcwd()


def word2html(root_dir):
    Application = wc.Dispatch('Word.Application')
    save_dir = root_dir + '\html'
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir,file)
        print file_path
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == '.doc' :
            doc = Application.Documents.Open(file_path)
            doc.SaveAs(save_dir + '\%s.html'%file[0:len(file)-4], 8)
            print save_dir + '\%s.html'%file[0:len(file)-4]
            doc.Close()

        if  os.path.isfile(file_path) and os.path.splitext(file_path)[1] == '.docx':
            doc = Application.Documents.Open(file_path)
            doc.SaveAs(save_dir + '\%s.htm'%file[0:len(file)-5], 8)
            print save_dir + '\%s.htm'%file[0:len(file)-5]
            doc.Close()

    Application.Quit()


if __name__ == "__main__":
    if not os.path.isdir(wordDir+"\word"):
        print u'请将word文档放置程序根目录下的word文件夹下'
        input = raw_input()
        exit()
    word2html(wordDir+"\word")
    print u'转换完成，回车退出'
    input = raw_input()
    exit()