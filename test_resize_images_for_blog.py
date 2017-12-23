import unittest
from resize_images_for_blog import *
import os

def create_test_env(_file_list):
    _dir = 'tmp'
    try:
        os.mkdir(_dir)
    except Exception as e:
        pass
    try:
        for _file in _file_list:
            _path = os.path.join(_dir,_file)
            _f = os.open(_path,os.O_CREAT)
            os.close(_f)
    except Exception as e:
        pass

def clean_test_env(_file_list):
    _dir = 'tmp'
    try:
        for _file in _file_list:
            _path = os.path.join(_dir,_file)
            os.remove(_path)
    except Exception as e:
        pass
    try:
        os.rmdir('tmp')
    except Exception as e:
        raise

class Test_resize_images_for_blog(unittest.TestCase):
    tmp_file_list = ['.DS_Store.jpg','1.jpg','2.jpg','3.jpg','file name.jpg']
    def setUp(self):
        create_test_env(self.tmp_file_list)

    def tearDown(self):
        clean_test_env(self.tmp_file_list)

    def test_check_str_raw_src_media_path(self):
        self.assertEqual(False,
                         check_str_raw_src_media_path(''))
        self.assertEqual(False,
                         check_str_raw_src_media_path('3.13123241'))
        self.assertEqual(True,
                         check_str_raw_src_media_path('tmp'))
        self.assertEqual(True,
                         check_str_raw_src_media_path('tmp '))
        self.assertEqual(True,
                         check_str_raw_src_media_path('"tmp "'))

    def test_rebuild_str_src_media_path(self):
        self.assertEqual('/path/subPath',
             rebuild_str_src_media_path('/path/subPath'))
        self.assertEqual('/path/subPath',
             rebuild_str_src_media_path('"/path/subPath"'))
        self.assertEqual('/path/subPath',
             rebuild_str_src_media_path('/path/subPath '))
        self.assertEqual('/path/sub\ Path',
             rebuild_str_src_media_path('/path/sub\ Path '))
        self.assertEqual('/path/sub\ Path',
             rebuild_str_src_media_path('"/path/sub\ Path "'))

    def test_get_str_list_src_images(self):
        self.assertEqual(self.tmp_file_list[1:],
             get_str_list_src_images('tmp'))

    def test_make_str_list_cmd_resize_images_fulls(self):
        # make_str_list_cmd_resize_images(_path,_dir,_src_image,_out_w,_out_h)
        _path = '/path/subPath'
        _dir = 'fulls'
        _src_image = '1.jpg'
        _out_w = '1200'
        _out_h = '750'
        _str_src_path = os.path.join(_path,_src_image)
        _str_output_path = os.path.join(_path,_dir,_src_image)
        '''
        _str_vf = ('scale=w={_out_w}:h={_out_h}:force_original_aspect_ratio=decrease,'
                   'pad=x=(ow-iw)/2:y=(oh-ih)/2:w={_out_w}:h={_out_h}')
        _str_vf= _str_vf.format_map(vars())
        # maybe use build str with keyWord,then split with keyWord to make list
        '''
        self.assertEqual(['sips',
                          _str_src_path,
                          '-s','format','jpeg',
                          '--resampleHeight','750',
                          '--padToHeightWidth','750','1200',
                          '--padColor','0D0D0D',
                          '-m','/System/Library/Colorsync/Profiles/sRGB Profile.icc',
                          '--out',_str_output_path],
             make_str_list_cmd_resize_images_fulls(_path,_dir,_src_image,_out_w,_out_h))

    def test_make_str_list_cmd_resize_images_thumbs(self):
        # make_str_list_cmd_resize_images_thumbs(_path,_dir,_src_image,_out_w,_out_h)
        _path = '/path/subPath'
        _dir = 'thumbs'
        _src_image = '1.jpg'
        _out_w = '300'
        _out_h = '300'
        _str_src_path = os.path.join(_path,_src_image)
        _str_output_path = os.path.join(_path,_dir,_src_image)
        self.assertEqual(['sips',
                          _str_src_path,
                          '-s','format','jpeg',
                          '--resampleHeight','300',
                          '--cropToHeightWidth','300','300',
                          '-m','/System/Library/Colorsync/Profiles/sRGB Profile.icc',
                          '--out',_str_output_path],
             make_str_list_cmd_resize_images_thumbs(_path,_dir,_src_image,_out_w,_out_h))

    def test_make_str_list_cmd_resize_images_thumbs_portrait(self):
        # make_str_list_cmd_resize_images_thumbs_portrait(_path,_dir,_src_image,_out_w,_out_h)
        _path = '/path/subPath'
        _dir = 'thumbs'
        _src_image = '1.jpg'
        _out_w = '300'
        _out_h = '300'
        _str_src_path = os.path.join(_path,_src_image)
        _str_output_path = os.path.join(_path,_dir,_src_image)
        self.assertEqual(['sips',
                          _str_src_path,
                          '-s','format','jpeg',
                          '--resampleWidth','300',
                          '--cropToHeightWidth','300','300',
                          '-m','/System/Library/Colorsync/Profiles/sRGB Profile.icc',
                          '--out',_str_output_path],
             make_str_list_cmd_resize_images_thumbs_portrait(_path,_dir,_src_image,_out_w,_out_h))

    def test_check_bool_image_is_portrait(self):
        # check_bool_image_is_portrait(_path,_src_image)
        self.assertEqual(True,
            check_bool_image_is_portrait('.','300x600.jpg'))
        self.assertEqual(False,
            check_bool_image_is_portrait('.','300x200.jpg'))
        self.assertEqual(False,
            check_bool_image_is_portrait('.','300x300.jpg'))



if __name__ == '__main__':
    unittest.main()
