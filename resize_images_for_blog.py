'''
Copy Right by likuku
likuku.public@gmail.com
last update on Dec18,2017
先决条件:
安装 ffmpeg-static, 路径加入当前用户 PATH 环境变量里
安装 python3
'''

import sys
import os
import subprocess
import time

print('需要 FFmpeg v3.3.x 和 Python v3.x :')

def get_str_raw_src_media_path_from_keyboard():
    _str_input_msg = '请输入素材图片目录路径 : '
    _str_raw_input = str(input(_str_input_msg))
    return(_str_raw_input)

def check_str_raw_src_media_path(_str_input):
    if len(_str_input) == 0:
        _bool_src_media_path = False
    else:
        _bool_src_media_path = os.access(_str_input.replace('"','').strip(),
                                         os.F_OK)
    return(_bool_src_media_path)

def rebuild_str_src_media_path(_str_input):
    _str_src_input = _str_input.replace('"','').strip()
    # 路径里包含空格，则拖拽文件时，windows 会自动给首尾加一对双引号，subprocess 不需要
    return(_str_src_input)

def get_str_list_src_images(_str_dir_path):
    _str_list = []
    with os.scandir(_str_dir_path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                _str_list.append(entry.name)
    return(_str_list)

def make_str_list_cmd_resize_images(_path,_dir,_src_image,_out_w,_out_h):
    ''' _dir is: full or thumbnail '''
    _str_list = []
    _str_src_path = os.path.join(_path,_src_image)
    _str_output_path = os.path.join(_path,_dir,_src_image)
    _str_vf = ('scale=w={_out_w}:h={_out_h}:force_original_aspect_ratio=decrease,'
               'pad=x=(ow-iw)/2:y=(oh-ih)/2:w={_out_w}:h={_out_h}')
    _str_vf= _str_vf.format_map(vars())
    _str_list = ['ffmpeg','-i',_str_src_path,'-pix_fmt','yuvj420p',
                 '-vf',_str_vf,'-q:v','2',_str_output_path]
    return(_str_list)

def main():
    _str_raw_path = get_str_raw_src_media_path_from_keyboard()
    if check_str_raw_src_media_path(_str_raw_path):
        _str_path = rebuild_str_src_media_path(_str_raw_path)
    else:
        print('素材目录无法访问，再次运行后,重新输入')
        time.sleep(2)
        exit()
    _str_list_src_images = get_str_list_src_images(_str_path)
    print(_str_list_src_images)
    if len(_str_list_src_images) <= 0:
        print('目录无素材，检查修正后再次运行')
        time.sleep(2)
        exit()
    else:
        pass
    try:
        os.mkdir(os.path.join(_str_path,'thumbnail'))
        os.mkdir(os.path.join(_str_path,'full'))
    except Exception as e:
        pass
    for _src_image in _str_list_src_images:
        # 1200x750 is full_size,360x225 is thumbnail_size, in demo
        _cmd_array_thumbnail = make_str_list_cmd_resize_images(_str_path,
                                                               'thumbnail',
                                                               _src_image,
                                                               '360','360')
        _cmd_array_full = make_str_list_cmd_resize_images(_str_path,
                                                          'full',
                                                          _src_image,
                                                          '1200','750')
        print(_cmd_array_thumbnail)
        print(_cmd_array_full)
        continue
        subprocess.call(_cmd_array_thumbnail)
        subprocess.call(_cmd_array_full)


if __name__ == '__main__':
    main()
