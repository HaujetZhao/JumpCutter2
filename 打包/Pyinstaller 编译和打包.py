# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Copyright (c) 2021 Haujet Zhao

import os
import sys
from icecream import ic
from shutil import copy, move, copytree, rmtree
import shlex
import subprocess
import glob, re
from pathlib import Path
from icecream import ic
from pprint import pprint
import platform

# 有两种打包方式
# 第一种是打包为一个大包
# 第二种是分成两个包，这种情况依赖于虚拟环境
# 两种都需要把相对导入改为绝对导入

# 当使用虚拟环境时两种方式都可以用，
# 当不使用虚拟环境时，只能用第一种。

# 对于小软件，使用第一种方式，打包成一个包就可以。
# 比如用到了人工智能库，打包出来可能有 1GB 大小，每次更新的时候都重新打包一遍就很浪费
# 就可以打包为两个包，其中一个是依赖库，另一个是源代码，每次更新只要更新原代码包就可以

使用虚拟环境 = True
源码分开打包 = True
依赖文件重新7z打包 = False

软件名字 = 'JumpCutter2'

# 源文件夹不要带空格，不要带减号，不要带中文，否则 pip 打包会失败
源码文件夹名 = 'JumpCutter2'
源码文件夹路径 = f'../{源码文件夹名}'
图标路径 = f'{源码文件夹名}/misc/icon.ico'
隐藏控制台 = False

需要单独复制的包 = [
    ]

# ====================函数区========================

def 复制(源, 目标, 过滤规则列表:list=None):
    # 得到源地址所有文件路径
    源文件集合 = set(glob.glob(str(Path(源) / '**'), recursive=True))

    # 将文件夹路径剃除
    for item in 源文件集合.copy():
        if os.path.isdir(item):
            源文件集合.remove(item)

    # 将要过滤的文件路径剃除
    if 过滤规则列表:
        for 过滤规则 in 过滤规则列表:
            过滤规则路径 = str(Path(源) / 过滤规则)
            过滤文件集合 = set(glob.glob(过滤规则路径, recursive=False))
            源文件集合 -= 过滤文件集合

    print('\n要复制的文件源路径：')
    pprint(源文件集合)
    print('\n')

    # 创建任务列表[
    #   [源1, 目标1]
    #   [源2, 目标2]
    #   ...
    # ]
    复制任务列表 = []
    for 源文件路径 in 源文件集合:
        目标文件路径 = str(Path(目标) / (Path(源文件路径).relative_to(源)))
        复制任务列表.append([源文件路径, 目标文件路径])

    for 任务 in 复制任务列表:
        if not Path(Path(任务[1]).parent).exists(): os.makedirs(Path(任务[1]).parent)
        copy(任务[0], 任务[1])
    ...

def 压缩到7z(源, 目标):
    if os.path.exists(目标): os.remove(目标)
    压缩命令 = f'7z a -t7z "{目标}" "{源}" -mx=9 -ms=200m -mf -mhc -mhcf  -mmt -r'
    命令参数 = shlex.split(压缩命令)
    subprocess.run(命令参数)

def 读取文本内容(文件路径):
    try:
        with open(文件路径, 'r', encoding='utf-8') as f:
            文本内容 = f.read()
    except:
        with open(文件路径, 'r', encoding='gbk') as f:
            文本内容 = f.read()
    return 文本内容

def 正则批量替换文件内容(文件名通配符, 搜索内容, 替换内容):
    for path in glob.glob(文件名通配符, recursive=True):
        print(f'\n开始正则替换：{path}\n搜索内容：{搜索内容}\n替换内容：{替换内容}')
        if not os.path.isfile(path): continue
        文本内容 = 读取文本内容(path)
        文本内容 = re.sub(搜索内容, 替换内容, 文本内容, flags=re.M)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(文本内容)

# ====================代码区========================

print(f'使用虚拟环境：{使用虚拟环境}')
print(f'源码分开打包：{源码分开打包}')
print(f'隐藏控制台：{隐藏控制台}')

启动器 = 'launcher'
启动器文件名 = f'{启动器}.py'

if not 使用虚拟环境:
    源码分开打包 = False

# 如果使用虚拟环境，就检查虚拟环境，如果没有，就创建，并安装依赖包
if 使用虚拟环境 and not os.path.exists('../pyvenv.cfg'):
    print(f'使用虚拟环境，但未发现虚拟环境，开始新建虚拟环境')
    命令 = f'python -m venv .'
    命令参数 = shlex.split(命令)
    subprocess.run(命令, cwd='..')

    print(f'更新 pip')
    命令 = f'"../Scripts/python" -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U'
    命令参数 = shlex.split(命令)
    subprocess.run(命令, cwd='..')

    命令 = f'"../Scripts/pip" install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller wheel'
    命令参数 = shlex.split(命令)
    subprocess.run(命令, cwd='..')

    print(f'开始在虚拟环境中安装依赖包')
    命令 = f'"../Scripts/pip" install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt'
    命令参数 = shlex.split(命令)
    subprocess.run(命令, cwd='..')



...

# 如果是虚拟环境
#   如果是分开打包
#       检查是否有依赖包
#           如果有就移动到备用地方
#           如果没有就拷贝一份
if 使用虚拟环境:
    if 源码分开打包:
        if os.path.exists(f'./dist/{启动器}/site-packages'):
            move(f'./dist/{启动器}/site-packages', f'./dist/site-packages')
            # move(f'./dist/{启动器名}/bin', f'./dist/bin')
        else:
            if not os.path.exists(f'./dist/site-packages'):
                print(f'正在从虚拟环境复制一份依赖包……')
                copytree(f'../Lib/site-packages', f'./dist/site-packages')

# 源代码中的依赖文件转移
源文件夹需要单独移动的文件夹列表 = ['bin', 'pretrained_models']
for 文件夹 in 源文件夹需要单独移动的文件夹列表:
    if os.path.exists(f'./dist/{启动器}/{文件夹}'):
        move(f'./dist/{启动器}/{文件夹}', f'./dist/{文件夹}') if os.path.exists(f'./dist/{启动器}/{文件夹}') else ...
    else:
        if not os.path.exists(f'./dist/{文件夹}'):
            print(f'正在从虚拟源代码文件夹复制二进制依赖包……')
            copytree(f'../{源码文件夹名}/{文件夹}', f'./dist/{文件夹}') if os.path.exists(f'../{源码文件夹名}/{文件夹}') else ...

# 准备临时原文件，将相对导入替换为绝对导入
临时源文件夹 = './dist/src'
if os.path.exists(临时源文件夹): rmtree(临时源文件夹)
排除列表 = [
    'bin/**/**',
    '__init__.py',
    '**/**.pyc',
    '**.ini',
    '**.db',
    'pretrained_models/**/**'
]
if Path(临时源文件夹).exists(): rmtree(临时源文件夹)
复制(源码文件夹路径, 临时源文件夹, 过滤规则列表=排除列表)
正则批量替换文件内容(f'{临时源文件夹}/**.py', r'(^\s*)import\s+\.(?=\w)', r'\1import ')
正则批量替换文件内容(f'{临时源文件夹}/**.py', r'(^\s*)from\s+\.(?=\w)', r'\1from ')
正则批量替换文件内容(f'{临时源文件夹}/**.py', r'(^\s*)from\s+\.\s+import', r'import')


# 如果是虚拟环境
#   如果是分开打包，准备 launcher.py，打包
#   如果是一个包，将 __main__.py 做成 launcher.py，打包
# 如果不是虚拟环境，将 __main__.py 做成 launcher.py，打包
启动器路径 = f'{临时源文件夹}/{启动器文件名}'
if 使用虚拟环境:
    if 源码分开打包:
        启动器内容 = '''import os
import sys
import pathlib

# 将 site-packages 目录导入 python 寻找 package 和 moduel 的变量
sys.path.append(str(pathlib.Path(os.path.abspath(__file__)).parent / 'site-packages')) 

import main
main.main()'''
        with open(启动器路径, 'w', encoding='utf-8') as f:
            f.write(启动器内容)

        隐藏控制台选项 = '-w' if 隐藏控制台 else ''
        图标选项 = f'-i "{图标路径}"' if os.path.exists(图标路径) else ''
        命令 = f'''"../Scripts/pyinstaller" --noconfirm {隐藏控制台选项} {图标选项}
                					--hidden-import distutils.version
                					--hidden-import uuid
                					--hidden-import distutils.version
                					--hidden-import imp
                					--hidden-import unittest.mock
                					--hidden-import cProfile
                					--hidden-import xml.etree
                					--hidden-import http.cookies
                					--hidden-import json
                					--hidden-import timeit
                					--hidden-import math
                                    --hidden-import wave
                                    --hidden-import site
                                    --hidden-import fractions
                                    --hidden-import timeit
                                    --hidden-import xml.dom
                                    --hidden-import importlib.resources
                                    --hidden-import ctypes.wintypes
                                    --hidden-import cgi
                					"{启动器路径}"
                '''
    else: # 一起打包
        move(f'{临时源文件夹}/__main__.py', 启动器路径)
        隐藏控制台选项 = '-w' if 隐藏控制台 else ''
        图标选项 = f'-i "{图标路径}"' if os.path.exists(图标路径) else ''
        命令 = f'''"../Scripts/pyinstaller" --noconfirm {隐藏控制台选项} {图标选项}
        					--hidden-import http.cookies
        					--hidden-import json
        					--hidden-import timeit
        					--hidden-import math
        					"{启动器路径}"
                '''
else: # 非虚拟环境打包
    move(f'{临时源文件夹}/__main__.py', 启动器路径)
    隐藏控制台选项 = '-w' if 隐藏控制台 else ''
    图标选项 = f'-i "{图标路径}"' if os.path.exists(图标路径) else ''
    命令 = f'''pyinstaller --noconfirm {隐藏控制台选项} {图标选项}
            					--hidden-import http.cookies
            					--hidden-import json
            					--hidden-import timeit
            					--hidden-import math
            					"{启动器路径}"
            '''
命令参数 = shlex.split(命令)
subprocess.run(命令参数)
os.remove(f'{临时源文件夹}/{启动器文件名}') # 删除 launcher.py
rmtree(f'{临时源文件夹}/__pycache__')
if 使用虚拟环境:
    if 源码分开打包:
        move(f'{临时源文件夹}/__main__.py', f'{临时源文件夹}/main.py')
复制(f'{临时源文件夹}', f'./dist/{启动器}') # 将源码相关文件复制到打包输出目录

if not 源码分开打包:

    # ic(需要单独复制的包)
    for package in 需要单独复制的包:
        for path in sys.path:
            if os.path.isdir(path):
                if package in os.listdir(path):
                    if os.path.exists(f'./dist/{启动器}/{package}'): rmtree(f'./dist/{启动器}/{package}')
                    copytree(Path(path) / package, f'./dist/{启动器}/{package}')
                    break

# 将依赖包移动到打包目录
if 源码分开打包:
    move(f'./dist/site-packages', f'./dist/{启动器}/site-packages')

# 源代码中的依赖文件转移
for 文件夹 in 源文件夹需要单独移动的文件夹列表:
    move(f'./dist/{文件夹}', f'./dist/{启动器}/{文件夹}') if os.path.exists(f'./dist/{文件夹}') else ...

# exe 重命名
exe文件名 = f'_{软件名字}.exe'
move(f'./dist/{启动器}/{启动器}.exe', f'./dist/{启动器}/{exe文件名}')

if 源码分开打包:
    # 7z 压缩依赖文件，如果依赖文件 7z 包存在，那就不压缩了

    包名 = f'依赖文件-{软件名字}_{platform.system()}.7z'
    if 依赖文件重新7z打包:
        if os.path.exists(包名): os.remove(包名)
        print(f'7z 压缩依赖包')
        压缩到7z(f'./dist/{启动器}/*', 包名)
        # 依赖文件-AudioSyncVideo_Windows.7z
        # 依赖文件-AudioSyncVideo_Windows.7z

    # 7z 压缩源文件
    包名 = f'源代码-{软件名字}_{platform.system()}.7z'
    if os.path.exists(包名): os.remove(包名)
    print(f'7z 压缩源代码')
    压缩到7z(f'{临时源文件夹}/*', 包名)

else: # 只打包一个包
    包名 = f'{软件名字}_{platform.system()}.7z'
    if 依赖文件重新7z打包:
        if os.path.exists(包名): os.remove(包名)
        print(f'7z 压缩整包')
        压缩到7z(f'./dist/{启动器}/*', 包名)
if platform.system() == 'Windows':
    exe绝对路径 = Path('.') / f'dist/{启动器}/{exe文件名}'
    os.system(f'explorer /select, "{exe绝对路径}"')
