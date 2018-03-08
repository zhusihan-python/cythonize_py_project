#encoding=utf-8

import os
import os.path
import shutil

#读入指定目录并转换为绝对路径
rootdir = input('root dir:\n')
rootdir = os.path.abspath(rootdir)
print('absolute root path:\n*** ' + rootdir + ' ***')
os.chdir(rootdir)

set_content = r'''from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


setup(
    cmdclass = {{'build_ext': build_ext}},
    ext_modules = [{}])]
)'''


def is_pyfile(filename):
    if filename.endswith('.py'):
        return True
    else:
        return False

#遍历目录，将py文件添加到setup文件中
for parent, dirnames, filenames in os.walk(rootdir):
    print(parent, dirnames, filenames)
    files_to_append = ''
    for filename in filenames:
        print(os.path.realpath(filename))
        cur_dir = os.path.split(os.path.realpath(filename))[0]
        # print(cur_dir)
        if is_pyfile(filename):
            cur_file = 'Extension({0}, [{1}]),'.format(filename.split('.')[0], filename)
            files_to_append += cur_file
    os.chdir(cur_dir)
    if files_to_append != '':
        print(os.getcwd())
        cur_set_content = set_content.format(files_to_append)
        setup_file = open('setup.py', 'w')
        setup_file.write(cur_set_content)
        setup_file.flush()
        setup_file.close()

#后修改目录名，这里注意topdown参数。
#topdown决定遍历的顺序，如果topdown为True，则先列举top下的目录，然后是目录的目录，依次类推；
#反之，则先递归列举出最深层的子目录，然后是其兄弟目录，然后父目录。
#我们需要先修改深层的子目录
# for parent, dirnames, filenames in os.walk(rootdir, topdown=False):
#     for dirname in dirnames:
#         pathdir = os.path.join(parent, dirname)
#         pathdirLower = os.path.join(parent, dirname.lower())
#         if pathdir == pathdirLower: #如果文件夹名本身就是全小写
#             continue
#         print(pathdir + ' --> ' + pathdirLower)
#         os.rename(pathdir, pathdirLower)