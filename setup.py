# 程序名
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Copyright (c) 2021 Haujet Zhao

from setuptools import setup

# python setup.py build sdist clean install & audio-video-resync
# twine upload -u USERNAME -p PASSWORD "dist/audio-video-resync-0.5.0.tar.gz"

setup(
    name='JumpCutter2',
    version='0.1.0',
    description='使用 spleeter 将视频中的人声提取出来（去除背景音），再对视频中的声音进行分析，分成静音部分和非静音部分，分别施加不同的速度，最后合成到一个新视频。',
    author='Haujet Zhao',
    author_email='haujetzhao@qq.com',
    url='https://github.com/HaujetZhao/JumpCutter2',
    license='MPL-2.0 License',
    
    # 依赖包
    install_requires=['av', 'spleeter', 'audiotsm', 'scipy', 'numpy'
        ],
    
    # 含有 py 文件的文件夹（源码文件夹）
    packages=['JumpCutter2', 'JumpCutter2/bin/Windows', 'JumpCutter2/bin/MacOS', 
            'JumpCutter2/pretrained_models/5stems'
        ],
    
    # 每个本地包中需要包含的另外的文件
    package_data={ 
        'JumpCutter2': ['*.md'],
        'JumpCutter2/bin/Windows': ['soundstretch*'],
        'JumpCutter2/bin/MacOS': ['soundstretch*'],
        'JumpCutter2/pretrained_models/5stems': ['*'],
        
        },
    
    # 安装后，命令行使用的入口
    entry_points={  # Options: console_scripts gui_scripts
            'console_scripts': [
                'JumpCutter2=JumpCutter2.__main__:main',
                '跳跃剪辑2=JumpCutter2.__main__:main', 
                '跳剪2=JumpCutter2.__main__:main'
            ]
    },
    
    platforms=["all"],
    
    classifiers=[  
        # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Pick your license as you wish
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3'
        ],
    
    # python 版本要求
    python_requires='>=3',

)

