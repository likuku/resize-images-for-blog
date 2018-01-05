'''
Copy Right by likuku
likuku.public@gmail.com
last update on Jan5,2018
先决条件:
安装 python3
'''

import sys
import os
import subprocess
import time

print('版本: v20180105_2137')
print('需要 Python v3.x :')
_msg = '''
图片列表文件格式:
一行一对前大图URL 后小图URL，之间用1空格分割，例如:
http://wx1.sinaimg.cn/large/4d48a5a9.jpg http://wx1.sinaimg.cn/large/4d58b5b9.jpg
http://wx1.sinaimg.cn/large/4d48a5b1.jpg http://wx1.sinaimg.cn/large/4d58b6b1.jpg
http://wx1.sinaimg.cn/large/4d48a5c2.jpg http://wx1.sinaimg.cn/large/4d58b7c2.jpg
'''
print(_msg)

def get_str_raw_src_media_path_from_keyboard():
    _str_input_msg = '请输入图片列表文件路径 : '
    _str_raw_input = str(input(_str_input_msg))
    return(_str_raw_input)

def check_str_raw_src_media_path(_str_input):
    if len(_str_input) == 0:
        _bool_src_media_path = False
    else:
        _bool_src_media_path = os.path.isfile(_str_input.replace('"','').strip())
    return(_bool_src_media_path)

def rebuild_str_src_media_path(_str_input):
    _str_src_input = _str_input.replace('"','').strip()
    # 路径里包含空格，则拖拽文件时，windows 会自动给首尾加一对双引号，subprocess 不需要
    return(_str_src_input)

def get_str_pixel_width_image(_str_img_url):
    _tmp_base = '/tmp'
    _img_name = _str_img_url.rsplit('/',1)[1]
    _tmp_img_path = os.path.join(_tmp_base,_img_name)
    _curl_get_cmd_array = ['curl','-s','-o',_tmp_img_path,_str_img_url]
    _get_pixel_width_cmd_array = ['sips',_tmp_img_path,'-g','pixelWidth']
    try:
        _obj_cmd = subprocess.Popen(_curl_get_cmd_array,shell=False,stdout=subprocess.PIPE)
        _obj_cmd.wait()
        _obj_cmd.stdout.close()
        _obj_cmd = subprocess.Popen(_get_pixel_width_cmd_array,shell=False,stdout=subprocess.PIPE)
        _obj_cmd.wait()
        _out_bytes_in_w = _obj_cmd.stdout.read()
        _obj_cmd.stdout.close()
        _int_w = int(_out_bytes_in_w.decode('utf-8').rsplit(' ',1)[1])
        _str_w = str(_int_w)
        os.remove(_tmp_img_path)
    except subprocess.CalledProcessError as e:
        print('[Error]: sips get pixel from image is crash.')
        raise e
    return(_str_w)

def main(_dev_mode):
    _str_raw_path = get_str_raw_src_media_path_from_keyboard()
    if check_str_raw_src_media_path(_str_raw_path):
        _str_list_url_img_path = rebuild_str_src_media_path(_str_raw_path)
    else:
        print('列表文件无法访问，再次运行后,重新输入')
        time.sleep(2)
        exit()
    _str_list_url_img_base_path = _str_list_url_img_path.rsplit('/',1)[0]
    _str_output_file = os.path.join(_str_list_url_img_base_path,'photos_html.txt')
    with open(_str_list_url_img_path, 'r') as _raw_list_file:
        _img_url_list = _raw_list_file.readlines()
        _num_total = len(_img_url_list)
        print(_num_total)
        with open(_str_output_file, 'wt') as _output_file:
            for _i in list(range(len(_img_url_list))):
                _num_do = _i + 1
                _str_progress = '[{_num_do}/{_num_total}] check photo,make html'
                _str_progress = _str_progress.format_map(vars())
                print(_str_progress,end='')
                _img_url_list[_i] = _img_url_list[_i].strip().split(' ')
                _full_img_url = _img_url_list[_i][0]
                _thumbs_img_url = _img_url_list[_i][1]
                _width = get_str_pixel_width_image(_thumbs_img_url)
                print('...',end='')
                _img_html = '<a href="{_full_img_url}" class="image"><img src="{_thumbs_img_url}" alt=""></a>'
                _img_html = _img_html.format_map(vars())
                _img_class = '<article class="item thumb" data-width="{_width}">'
                _img_class = _img_class.format_map(vars())
                print(_img_class, file = _output_file)
                print('<h2></h2>', file = _output_file)
                print(_img_html, file = _output_file)
                print('</article>', file = _output_file)
                print('Done')
    print('Photos html code in %s' % _str_output_file)
    print('Great! All Done')


if __name__ == '__main__':
    _dev_mode = True
    main(_dev_mode)
