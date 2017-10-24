# -*- coding: utf-8 -*-

import time


class Log():
    @staticmethod
    def write(val):
        filename = time.strftime('%Y%m%d%H', time.localtime(time.time()))
        cur_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        with open('./log/%s.txt' % filename, 'w') as fp:
            fp.write('%s-->%s\n' % (cur_time, val))
            fp.close()


if __name__ == "__main__":
    print Log.write('ad')
