from os import listdir
from os import walk
from os.path import join
import sys

# TODO
# - get versions if installed
# - write to requirements.txt
# - ignore more builtin modules

OTHER_BUILTINS = ['os','urllib2', 'collections', 'multiprocessing','subprocess','distutils','json','functools','dateutil','datetime']
BUILTINS = set(sys.builtin_module_names).union(OTHER_BUILTINS)

def dir_iter(location):
    files = []
    for (dirpath, dirnames, filenames) in walk(location):
        files.extend(map(lambda x: join(dirpath,x), filter(lambda x: not x.startswith('.'), filenames)))
    return files

def get_reqs(location):
    if isinstance(location,file):
        return get_reqs_file(location)
    if isinstance(location, basestring):
        reqs = set()
        filenames = dir_iter(location)
        if filenames:
            for i in filenames:
                reqs = reqs.union(get_reqs(i))
        else:
            with open(location, 'r') as f:
                reqs = reqs.union(get_reqs_file(f))
        return list(reqs)

def get_reqs_file(f):
    reqs = set()
    module = f.read().split('\n')
    for line in module:
        reqs_list = []
        if 'import' == line.strip()[:6]:
            if line.find(',') > 0:
                req = [i.strip().split('.')[0] for i in line.replace('import ','').strip().split(',')]
            else:
                if line.find(' as ') > 0:
                    req = line[line.find('import')+7:line.find(' as')].split('.')[0].strip()
                else:
                    req = line.replace('import','').strip()
        elif 'from' == line.strip()[:4]:
            req = line[line.find('from')+4:line.find('import')].strip().split('.')[0]
        else:
            continue
        if type(req) == str:
            if req not in BUILTINS:
                reqs.add(req)
        elif type(req) == list:
            for r in req:
                if r not in BUILTINS:
                    reqs.add(r)
    return reqs

if __name__=="__main__":
    print get_reqs(sys.argv[1])
