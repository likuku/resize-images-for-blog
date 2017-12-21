'''
Copy Right by likuku
likuku.public@gmail.com
last update on Dec21,2017
先决条件:
安装 python3
'''

import sys
import os
import subprocess
import time

print('需要 Python v3.x :')

def get_str_raw_src_media_path_from_keyboard():
    _str_input_msg = '请输入素材图片目录路径 : '
    _str_raw_input = str(input(_str_input_msg))
    return(_str_raw_input)

def check_str_raw_src_media_path(_str_input):
    if len(_str_input) == 0:
        _bool_src_media_path = False
    else:
        _bool_src_media_path = os.path.isdir(_str_input.replace('"','').strip())
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

def make_str_list_cmd_resize_images_fulls(_path,_dir,_src_image,_out_w,_out_h):
    ''' _dir is: fulls or thumbs '''
    _str_list = []
    _str_src_path = os.path.join(_path,_src_image)
    _str_output_path = os.path.join(_path,_dir,
                                    os.path.splitext(_src_image)[0]+'.jpg')
    # webColor: 0D0D0D means light is 5% or dark is 95%
    _str_list = ['sips',
        _str_src_path,
        '-s','format','jpeg',
        '--resampleHeight',_out_h,
        '--padToHeightWidth',_out_h,_out_w,
        '--padColor','0D0D0D',
        '-m','/System/Library/Colorsync/Profiles/sRGB Profile.icc',
        '--out',_str_output_path]
    return(_str_list)

def make_str_list_cmd_resize_images_thumbs(_path,_dir,_src_image,_out_w,_out_h):
    ''' _dir is: thumbs '''
    _str_list = []
    _str_src_path = os.path.join(_path,_src_image)
    _str_output_path = os.path.join(_path,_dir,
                                    os.path.splitext(_src_image)[0]+'.jpg')
    _str_list = ['sips',
        _str_src_path,
        '-s','format','jpeg',
        '--resampleHeight','300',
        '--cropToHeightWidth','300','300',
        '-m','/System/Library/Colorsync/Profiles/sRGB Profile.icc',
        '--out',_str_output_path]
    return(_str_list)

def make_str_list_cmd_resize_images_thumbs_portrait(_path,_dir,_src_image,_out_w,_out_h):
    pass

def check_bool_image_is_portrait(_path,_src_image):
    pass

def main():
    _str_raw_path = get_str_raw_src_media_path_from_keyboard()
    if check_str_raw_src_media_path(_str_raw_path):
        _str_path = rebuild_str_src_media_path(_str_raw_path)
    else:
        print('素材目录无法访问，再次运行后,重新输入')
        time.sleep(2)
        exit()
    _str_list_src_images = get_str_list_src_images(_str_path)
    if len(_str_list_src_images) <= 0:
        print('目录无素材，检查修正后再次运行')
        time.sleep(2)
        exit()
    else:
        pass
    try:
        os.mkdir(os.path.join(_str_path,'thumbs'))
        os.mkdir(os.path.join(_str_path,'fulls'))
    except Exception as e:
        pass
    for _src_image in _str_list_src_images:
        # 1200x750 is full_size,360x225 is thumbnail_size, in demo
        _cmd_array_thumbs = make_str_list_cmd_resize_images(_str_path,
                                                               'thumbs',
                                                               _src_image,
                                                               '360','360')
        _cmd_array_fulls = make_str_list_cmd_resize_images(_str_path,
                                                          'fulls',
                                                          _src_image,
                                                          '1200','750')
        print(_cmd_array_thumbs)
        print(_cmd_array_fulls)
        continue
        subprocess.call(_cmd_array_thumbs)
        subprocess.call(_cmd_array_fulls)


if __name__ == '__main__':
    main()
