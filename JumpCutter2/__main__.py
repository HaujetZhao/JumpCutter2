#coding=utf-8

# JumpCutter2
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021 Haujet Zhao

# 内存分析：
# @profile
# python -m memory_profiler __main__.py

import argparse
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from . import JumpCut

# 这里从相对路径导入，在被 pyinstaller 打包时，需要换成绝对路径

def main():
    没有参数 = False
    if len(sys.argv) == 1:
        没有参数 = True

        print(f'''
你没有输入任何文件，因此进入文字引导。
你可以在命令行加上 -h 参数运行此程序以获得
命令行运行的帮助。

程序的用处主要是对视频中的声音进行分析，
分成静音部分和非静音部分，
分别施加不同的速度，最后合成到一个新视频。
''')
        print(f'\n请输入要处理的视频或音频文件')
        sys.argv.append(得到输入文件())

    parser = argparse.ArgumentParser(
        description='''功能：对视频中的声音进行分析，分成静音部分和非静音部分，分别施加不同的速度，最后合成到一个新视频。''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument('File', nargs='+',  type=str, help='要处理的音频或视频文件，可一次添加多个文件')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--suffix', metavar='Suffix', type=str, default='_JumpCut', help='处理后生成的文件名后缀')
    parser.add_argument('--silence-speed', metavar='Speed', type=float, default=8.0, help='静音片段速度')
    parser.add_argument('--sounded-speed', metavar='Speed', type=float, default=1.0, help='有声片段速度')
    parser.add_argument('--buffer-frame', metavar='Number', type=int, default=4, help='片段间缓冲帧数')
    parser.add_argument('--threshold', metavar='Threshold', type=float, default=0.04, help='声音检测相对阈值')
    parser.add_argument('--codec', metavar='Codec', type=str, default='libx264', help='视频编码器')
    parser.add_argument('--crf', metavar='Number', type=float, default=23.0, help='视频质量crf参数')
    parser.add_argument('--only-audio',action='store_true', help='只处理音频')
    parser.add_argument('--aux', metavar='File', type=str, default='', help='辅助音频文件')
    parser.add_argument('--no-spleeter',action='store_true', help='不要使用 spleeter 生成辅助音频文件')
    args = parser.parse_args()

    if 没有参数:
        得到参数(args)

    处理(args)

    if 没有参数:
        input('\n所有任务处理完毕，按下回车结束程序')

def 得到参数(args):
    args.silence_speed = 得到静音片段速度(args.silence_speed)
    args.sounded_speed = 得到有声片段速度(args.sounded_speed)
    确认参数(args)

def 确认参数(args):
    用户输入 = input(f'''\n得到以下处理参数：\n
1. 输入文件：{args.File[0]}
2. 输出文件后缀：{args.suffix}\n
3. 静音片段速度：{args.silence_speed}
4. 有声片段速度：{args.sounded_speed}\n
5. 片段间缓冲帧数：{args.buffer_frame}
6. 声音检测相对阈值：{args.threshold}\n
7. 视频编码器：{args.codec}
8. 视频质量crf参数：{args.crf}\n
9. 只处理音频：{args.only_audio}
10. 辅助音频文件：{args.aux}\n
11. 使用 spleeter 生成辅助音频文件：{not args.no_spleeter}\n
如果确认正确，请回车继续，接下来将开始视频处理；
而如果有参数不正确，需要修改，请输入对应的序号，再回车：\n\n''')
    try:
        if 用户输入 == '':
            return
        else:
            int(用户输入)
    except:
        return
    if int(用户输入) == 1:
        args.File[0] = 得到输入文件()
    elif int(用户输入) == 2:
        args.suffix = 得到输出后缀(args.suffix)

    elif int(用户输入) == 3:
        print(f'sil_sp: {args.silence_speed}')
        args.silence_speed = 得到静音片段速度(args.silence_speed)
    elif int(用户输入) == 4:
        args.sounded_speed = 得到有声片段速度(args.sounded_speed)

    elif int(用户输入) == 5:
        args.buffer_frame = 得到片段间缓冲帧数(args.buffer_frame)
    elif int(用户输入) == 6:
        args.threshold = 得到声音检测相对阈值(args.threshold)

    elif int(用户输入) == 7:
        args.codec = 得到视频编码器(args.codec)
    elif int(用户输入) == 8:
        args.crf = 得到视频质量crf参数(args.crf)

    elif int(用户输入) == 9:
        args.only_audio = 得到只处理音频(args.only_audio)
    elif int(用户输入) == 10:
        args.aux = 得到辅助音频文件(args.aux)
    elif int(用户输入) == 11:
        args.no_spleeter = 得到使用spleeter生成辅助音频(args.no_spleeter)
    else:
        return
    确认参数(args)

def 得到输入文件():
    while True:
        用户输入 = input(f'请输入文件路径 或 直接拖入：')
        if 用户输入 == '':
            continue
        if os.path.exists(用户输入.strip('\'"')):
            输入文件 = 用户输入.strip('\'"')
            break
        else:
            print('输入的文件不存在，请重新输入')
    return 输入文件

def 得到输出后缀(默认值):
    return 得到字符串(f'请输入输出文件的后缀', 默认值)

def 得到静音片段速度(默认值):
    return 得到小数(f'\n请输入静音片段速度：', 默认值, 0.10, 9999999999999999)

def 得到有声片段速度(默认值):
    return 得到小数(f'\n请输入有声片段速度：', 默认值, 0.10, 9999999999999999)

def 得到片段间缓冲帧数(默认值):
    return 得到整数(f'\n请输入片段间缓冲帧数：', 默认值, 0, 30)

def 得到声音检测相对阈值(默认值):
    return 得到小数(f'\n请输入声音检测相对阈值：', 默认值, 0.0, 1.0)

def 得到视频编码器(默认值):
    return 得到字符串(f'\n请输入视频编码器：\n    libx264 速度快\n    libx265 体积小', 默认值)

def 得到视频质量crf参数(默认值):
    return 得到整数(f'\n请输入视频质量crf参数，越低画质越好，同时体积越大：', 默认值, 0, 51)

def 得到只处理音频(默认值):
    return 得到布尔值(f'\n请输入是否只处理音频，如果是的话，会忽略处理视频。', 默认值)

def 得到辅助音频文件(默认值):
    while True:
        辅助音频文件 = 得到字符串('\n如果有辅助音频（比如去除了背景音的音频轨），你可以在这里输入，直接回车表示为空', '').strip('\'"')
        if 辅助音频文件 != '' and not os.path.exists(辅助音频文件):
            print(f'您输入的音频文件路径不存在，请重新输入')
            continue
        break
    return 辅助音频文件

def 得到使用spleeter生成辅助音频(默认值):
    return not 得到布尔值('\n是否使用 spleeter 生成辅助音频文件用于分段？', 默认值)

def 检查目标文件路径(路径):
    目标文件夹Path = Path('路径').parent
    if not 目标文件夹Path.exists():
        目标文件夹Path.mkdir(parents=True)

def 得到整数(提示语, 默认值: int, 最小值: int, 最大值: int):
    while True:
        数值 = input(提示语 + f'\n    (默认值：{默认值}   有效数值：{最小值} ~ {最大值})\n')
        if 数值 == '':
            return 默认值
        try:
            数值 = int(数值)
        except:
            print('您的输入不是有效数字，请重新输入')
            continue
        if 数值 < 最小值 or 数值 > 最大值:
            print('您输入的值不在有效范围内，请重新输入')
            continue
        break
    return 数值

def 得到小数(提示语, 默认值: float, 最小值: float, 最大值: float):
    while True:
        数值 = input(提示语 + f'\n    (默认值：{默认值}   有效数值：{最小值} ~ {最大值})\n')
        if 数值 == '':
            return 默认值
        try:
            数值 = float(数值)
        except:
            print('您的输入不是有效数字，请重新输入')
            continue
        if 数值 < 最小值 or 数值 > 最大值:
            print('您输入的值不在有效范围内，请重新输入')
            continue
        break
    return 数值

def 得到字符串(提示语, 默认值: str):
    数值 = input(提示语 + f'\n    (默认值：{默认值})\n')
    if 数值 == '':
        return 默认值
    return 数值

def 得到布尔值(提示语, 默认值: bool):
    用户回应 = input(提示语 + f'\n    (默认值：{默认值})\n    输入 1、y、True 表示“是”；输入 0, n, False 或表示“否”；其它值或直接回车为默认\n').lower()
    if 用户回应 == '1' or 用户回应 == 'y' or 用户回应 == 'true':
        return True
    elif 用户回应 == '0' or 用户回应 == 'n' or 用户回应 == 'false':
        return False
    else:
        return 默认值

def 得到临时文件夹(文件):
    return tempfile.mkdtemp(dir=os.path.dirname(文件), prefix=Path(文件).stem)


def 处理(参数:argparse.ArgumentParser):

    # 如果有多个视频需要处理，一个辅助文件显然是不行的
    if len(参数.File) > 1: 参数.aux = ''

    if 参数.no_spleeter:
        分轨器 = False
    else:
        print(f'正在导入 spleeter')
        from spleeter.separator import Separator
        spleeter辅助音频文件名 = 'vocal.wav'
        # 模型要放到 pretrained_models 文件夹中
        spleeter使用模型名称 = '5stems'
        模型父文件夹 = Path(Path(__file__).parent)
        os.chdir(模型父文件夹)
        print(f'spleeter 模型所在文件夹：{Path(模型父文件夹) / "pretrained_models"}')
        分轨器 = Separator(f'spleeter:{spleeter使用模型名称}', multiprocess=False)

    # 依次处理这些视频
    for index, File in enumerate(参数.File):
        print(f'总共有 {len(参数.File)} 个文件需要处理，正在处理第 {index + 1} 个：{File}')
        处理文件(File, 参数, 分轨器)

def 处理文件(file, 参数:argparse.ArgumentParser, 分轨器):
    输出文件 = os.path.splitext(file)[0] + 参数.suffix + os.path.splitext(file)[1]
    临时文件夹 = 得到临时文件夹(输出文件)
    JumpCut.跳剪(file,
                 输出文件=输出文件,
                 静音速度=参数.silence_speed,
                 有声速度=参数.sounded_speed,
                 缓冲帧数=参数.buffer_frame,
                 有声阈值=参数.threshold,
                 视频编码器=参数.codec,
                 crf画质参数=参数.crf,
                 只处理音频=参数.only_audio,
                 辅助音频文件=参数.aux,
                 使用spleeter=分轨器,
                 临时文件夹=临时文件夹)

if __name__ == '__main__':
    main()