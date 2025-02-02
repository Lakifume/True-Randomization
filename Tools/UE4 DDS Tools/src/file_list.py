import os

'''
format

1st line: folder path
2nd line: uasset
3rd line: dds
4th line: uasset
5th line: dds
    :      :

'''

'''
example

if file_list.txt is

foo/bar/
uexp/a.uasset
dds/d.dds
test/ppp.uasset
b/ttt.dds

then DDS tool will inject

foo/bar/dds/d.dds into foo/bar/uexp/a.uasset
foo/bar/b/ttt.dds into foo/bar/test/ppp.uasset
'''

def remove_quotes(l):
    if l[-1]=='\n':
        l=l[:-1]
    if l in ['', '"']:
        return ''
    if l[0]=='"':
        l=l[1:]
    if l[-1]=='"':
        l=l[:-1]
    return l

def get_file_list_from_txt(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    lines = [remove_quotes(l) for l in lines]
    lines = [l for l in lines if l!='']
    folder = lines[0]
    file_list = lines[1:]

    directory, folder = get_base_folder(folder)
    file_list = [os.path.join(folder, file) for file in file_list]
    return directory, file_list

def get_base_folder(p):
    folder = os.path.basename(p)
    directory = os.path.dirname(p)
    if folder=="":
        folder = os.path.dirname(directory)
        directory = os.path.basename(directory)  
    if directory==".":
        directory=""
    return directory, folder

def get_ext(path):
    return path.split('.')[-1].lower()

def get_file_list_from_folder(folder, ext=None, include_base=True):
    file_list = get_file_list_rec(folder)
    if ext is not None:
        file_list = [f for f in file_list if get_ext(f) in ext]
    if include_base:
        directory, folder = get_base_folder(folder)
        file_list = [os.path.join(folder, file) for file in file_list]
    else:
        directory = folder
    return directory, file_list

def get_file_list_rec(folder):
    file_list=[]
    for file in sorted(os.listdir(folder)):
        file_path = os.path.join(folder, file)
        if os.path.isdir(file_path):
            file_list+=[os.path.join(file, f) for f in get_file_list_rec(file_path)]
        else:
            file_list.append(file)
    return file_list

