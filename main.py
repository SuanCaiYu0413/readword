# -*- coding: utf-8 -*-
import rws_parse
import sbs_parse
import yss_parse
with open(r'.\html\10rkx0002rws\10rkx0002rws.html') as fp:
    html = fp.read()
    fp.close()

rws = rws_parse.rws(html)
print rws.parse()
with open(r'.\html\10rkx0002sbs\10rkx0002sbs.html') as fp:
    html = fp.read()
    fp.close()
sbs = sbs_parse.sbs(html)

print sbs.parse()

with open(r'.\html\10rkx0002yss\10rkx0002yss.html') as fp:
    html = fp.read()
    fp.close()
yss = yss_parse.yss(html)

yss.parse()