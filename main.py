import os
import sys
import re
import json


class Mapping:

    __name__ = 'Mapping'
    path_list = []
    db = 'maps.json'
    data = None

    # json
    # ============
    # {
    #   'fn':{'fl':1,'fp':'xxx.php','fa':['a','b','c'],'ff':['xxx','yyy','zzz']}
    # }
    #

    def __init__(self):
        self.debug = False
        # database
        if not os.path.exists(self.db):
            self.save({})
        if not self.data:
            self.read()

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

    def add_func(self, fn, fl, fp, fa, ff):
        self.data[fn] = {}
        self.data[fn]['fl'] = fl
        self.data[fn]['fp'] = fp
        self.data[fn]['fa'] = fa
        self.data[fn]['ff'] = ff

    def del_func(self, func):
        del self.data[func]

    def sel_func(self, func):
        return self.data[func]

    # database end

    # Analysis

    def search_tag(self, pos, cont):
        self.op('search_tag_pos:', pos)
        # cont = cont[pos:]
        p = cont[pos:].find('{') + 1
        level = 1
        while(level != 0):
            a = cont[pos + p:].find('{') + 1
            b = cont[pos + p:].find('}') + 1
            self.op('a:', a, 'b:', b)
            if a != -1:
                level = level + 1
            if b != -1:
                level = level - 1
            if b > a:
                level = level - 1
                p = p + a
            else:
                p = p + b
            self.op('level:', level)
            raw_input('---------')
        return pos + p

    def analysis_files(self, filepathlist):
        for filepath in filepathlist:
            path = filepath.replace('\n', '')
            with open(path, 'r') as f:
                self.this_path = path
                self._analysis_file(f.read())

    def _analysis_file(self, content):
        self.op(self.this_path, len(content))
        pos = 0
        while(content[pos:].find('function ') != -1):
            self.op("pos:", pos)
            # fn
            pos_s = content[pos:].find('function ') + pos + 9
            self.op("pos_s:", pos_s)
            pos_e = content[pos_s:].find('(') + pos_s
            self.op("pos_e", pos_e)
            fn = content[pos_s:pos_e].replace(' ', '')
            self.op("fn:", fn)
            # fl
            fl = content[:pos_e].count('\n') + 1
            self.op("fl:", fl)
            # fa
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
            # ff
            ff = []
            # tag
            pos = self.search_tag(pos, content)
            # pos = pos_e
            self.add_func(fn, fl, self.this_path, fa, ff)

    # Analysis end

if __name__ == '__main__':
    m = Mapping()
    m.debug = True
    # m.mapping('/Users/virink/www')
    m.mapping('/Users/virink/Workspace/AutoAuditHelper/Func_Mapping')
    m.show_maps()
    # os.system('pwd')
