from os import listdir
from os import walk
from os.path import join

# TODO
# - handle all import formats
# ++ from .. import .. as ..
# ++ import .. as ..
# ++ import X,Y
# - get versions if installed
# - write to requirements.txt
# - ignore builtin modules

def dir_iter(location):
    files = []
    for (dirpath, dirnames, filenames) in walk(location):
        files.extend(map(lambda x: join(dirpath,x), filter(lambda x: not x.startswith('.'), filenames)))
    return files

def get_reqs(location):
    if isinstance(location,file):
        return get_reqs_file(location)
    if isinstance(location, basestring):
        reqs = []
        filenames = dir_iter(location)
        if filenames:
            for i in filenames:
                reqs.extend(get_reqs(i))
        else:
            with open(location, 'r') as f:
                reqs.extend(get_reqs_file(f))
        return reqs

def get_reqs_file(f):
    reqs = set()
    module = f.read().split('\n')
    for line in module:
        if 'import' == line.strip()[:6]:
            req = line.replace('import ','')
        elif 'from' == line.strip()[:4]:
            req = line[5:line.find('import')-1]
        reqs.add(req)
    return reqs

if __name__=="__main__":
    import sys
    print get_reqs(sys.argv[1])
