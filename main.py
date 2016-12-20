# -*- coding: UTF-8 -*-

import os
from itertools import chain
import json
import re

__Author__ = 'Virink'


class Mapping:

    __name__ = 'Mapping'
    db = 'maps.json'

    # json
    # ============
    # {
    #   'fn':{'fl':1,'fp':'xxx.php','fa':['a','b','c'],'ff':{1:'xx',2:'yy'}, 'fr':'xxxxx', 'fb':'xxxxx'}
    # }
    #

    def __init__(self):
        self.debug = False
        # database
        if not os.path.exists(self.db):
            self.save({})
        self.data = {}
        with open('pif.dat', 'r') as f:
            self.pif = f.readlines()
        for i in xrange(len(self.pif)):
            self.pif[i] = self.pif[i].strip()
        # if not self.data:
        #     self.read()

    # Mapping

    def op(self, a, *b):
        if not self.debug:
            return ''
        print a,
        for i in b:
            print i,
        print ''

    def mapping(self, path):
        if path == '':
            self.log(2, 'path is null')
            return ''
        # get filepath
        self.walk_dir(path)
        # analysis file
        self.analysis_files(self.path_list)

    def show_maps(self):
        for k in self.data.keys():
            print k, ':', self.data[k]

    def walk_dir(self, root):
        # 'find  ' + path + '| egrep "\.php|inc"'
        os.system('find  ' + root + '| egrep "\.php|inc" > ' +
                  root + '/walk_dir.tmp')
        with open(root + '/walk_dir.tmp') as f:
            self.path_list = f.readlines()
        os.system('rm ' + root + '/walk_dir.tmp')
        # for l in self.path_list:
        #     print l,

    def log(self, l=2, msg='log error'):
        level = ['Debug', 'Info', 'Error']
        print __name__ + ' ' + level[l] + ' : ' + msg

    # Mapping end

    # database

    def read(self):
        with open(self.db, 'r') as f:
            self.data = json.loads(f.read())

    def save(self):
        with open(self.db, 'w') as f:
            f.write(json.dumps(self.data))

    def add_func(self, fn, fl, fp, fa, fb, fr):
        self.data[fn] = {}
        self.data[fn]['fl'] = fl  # function lineno
        self.data[fn]['fp'] = fp  # function filepath
        self.data[fn]['fa'] = fa  # function args
        self.data[fn]['fb'] = fb  # function body
        self.data[fn]['fr'] = fr  # function return

    def del_func(self, func):
        del self.data[func]

    def sel_func(self, func):
        return self.data[func]

    # database end

    # Analysis

    def analysis_files(self, filepathlist):
        for filepath in filepathlist:
            path = filepath.replace('\n', '')
            with open(path, 'r') as f:
                self.this_path = path
                self._analysis_file(f.read())

    def _analysis_file(self, content):
        self.op(self.this_path, len(content))
        # Clean Comments
        m_comments = re.findall(r'(/\*.*?\*/)', content, re.S)
        if m_comments:
            for i in m_comments:
                content = content.replace(i, '\n' * i.count('\n'))
        m_comments = re.findall(r'(//.*)', content)
        if m_comments:
            for i in m_comments:
                content = content.replace(i, '')
        #####################
        # with open('test.bak.php', 'w') as f:
        #     f.write(content)
        # # Search Function
        # m_funcs = re.findall(
        #     r'function\s*([a-z0-9_]*)\s*\((.*?)\)\{(.*?)\}', content, re.S)
        # # print m_funcs
        # for i in m_funcs:
        #     self.op(i)
        #     # function name
        #     fn = i[0]
        #     # function args
        #     tmp_fa = i[1].replace(' ', '')
        #     if tmp_fa == '':
        #         fa = []
        #     elif ',' in tmp_fa:
        #         fa = tmp_fa.split(',')
        #     else:
        #         fa = [tmp_fa]
        #     fl = content[:content.find(fn)].count('\n') + 1
        #     fb = i[2].replace('\n', '')
        #     if 'return' in fb:
        #         m_return = re.findall(r'return (.*?);', fb)
        #         fr = m_return[0]
        #         self.op(fr)
        #     else:
        #         fr = ''
        #########################
        pos = 0
        while(content[pos:].find('function ') != -1):
            self.op("pos:", pos)
            # function name
            pos_s = content[pos:].find('function ') + pos + 9
            self.op("pos_s:", pos_s)
            pos_e = content[pos_s:].find('(') + pos_s
            self.op("pos_e", pos_e)
            fn = content[pos_s:pos_e].replace(' ', '')
            self.op("fn:", fn)
            # function lineno
            fl = content[:pos_e].count('\n') + 1
            self.op("fl:", fl)
            # function args
            pos_a = content[pos_e + 1:].find(')') + pos_e + 1
            tmp_fa = content[pos_e + 1:pos_a].replace(' ', '')
            self.op("tmp_fa:", tmp_fa)
            if tmp_fa == '':
                fa = []
            elif ',' in tmp_fa:
                fa = tmp_fa.split(',')
            else:
                fa = [tmp_fa]
            self.op("fa:", fa)
            # function body
            level = 1
            self.op('pos_a:', pos_a)
            pos_t = content[pos_a:].find('{') + 1 + pos_a
            pos = pos_t
            self.op('pos:', pos)
            while(level != 0):
                a = content[pos:].find('{')
                b = content[pos:].find('}')
                self.op('a:', a, 'b:', b)
                if a != -1:
                    level = level + 1
                if b != -1:
                    level = level - 1
                if a == -1:
                    pos = pos + b + 1
                    continue
                if b > a:
                    pos = pos + a + 1
                else:
                    level = level - 1
                    pos = pos + b + 1
                self.op('pos:', pos)
                self.op('level:', level)
            fb = content[pos_t:pos - 1]
            # function return
            if 'return' in fb:
                m_return = re.findall(r'return (.*?);', fb)
                fr = m_return[0]
                self.op(fr)
            else:
                fr = ''
            self.add_func(fn, fl, self.this_path, fa, fb, fr)
            self.op('--------------------')

    def func_in_func(self):
        fcf = self.data.keys()
        aff = list(set(chain(fcf, self.pif)))
        for cf in fcf:
            tmp_f = []
            for f in aff:
                if f + "(" in self.data[cf]['fb']:
                    tmp_f.append(f)
            tmp_i = {}
            tmp_s = []
            i = 1
            for tf in tmp_f:
                n = self.data[cf]['fb'].find(tf)
                tmp_i[n] = tf
                tmp_s.append(n)
            tmp_s.sort()
            ff = {}
            for s in tmp_s:
                ff[i] = tmp_i[s]
                i += 1
            self.data[cf]['ff'] = ff
        self.save()

    # Analysis end

if __name__ == '__main__':
    m = Mapping()
    # m.debug = True
    # m.mapping('/Users/virink/www')
    m.mapping('.')
    m.func_in_func()
    m.show_maps()
    # os.system('pwd')
    m.save()
