from os import listdir
from os import walk

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
        files.extend(filenames)
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
    reqs = []
    module = f.readlines()
    for line in module:
        if 'import' in line:
            reqs.append(line.replace('import ','').replace('\n',''))
    return reqs

if __name__=="__main__":
    import sys
    print get_reqs(sys.argv[1])
