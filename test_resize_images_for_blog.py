import unittest
from resize_images_for_blog import *
import os

def create_test_env():
    print ('create_test_env:')
    try:
        os.mkdir('./tmp')
        f = os.open('./tmp/1.jpg')
        f.close()
        f = os.open('./tmp/2.jpg')
        f.close()
        f = os.open('./tmp/3.jpg')
        f.close()
    except Exception as e:
        pass

def clean_test_env():
    try:
        os.remove('./tmp/*')
    except Exception as e:
        pass
    try:
        os.rmdir('./tmp')
    except Exception as e:
        pass

class Test_resize_images_for_blog(unittest.TestCase):
    def test_check_str_raw_src_media_path(self):
        self.assertEqual(False,
                         check_str_raw_src_media_path(''))
        self.assertEqual(False,
                         check_str_raw_src_media_path('.13123241'))
        self.assertEqual(True,
                         check_str_raw_src_media_path('.'))

    def test_rebuild_str_src_media_path(self):
        self.assertEqual('/path/subPath',
             rebuild_str_src_media_path('/path/subPath'))
        self.assertEqual('/path/subPath',
             rebuild_str_src_media_path('"/path/subPath"'))
        self.assertEqual('/path/subPath',
             rebuild_str_src_media_path('/path/subPath '))
        self.assertEqual('/path/sub\ Path',
             rebuild_str_src_media_path('/path/sub\ Path '))

    def test_get_str_list_src_images(self):
        self.assertEqual(['1.jpg','2.jpg','3.jpg'],
             get_str_list_src_images('./tmp'))

    def make_str_list_cmd_resize_images(self):
        # make_str_list_cmd_resize_images(_path,_dir,_src_image,_out_w,_out_h)
        _path = '/path/subPath'
        _dir = 'full'
        _src_image = '1.jpg'
        _out_w = '1920'
        _out_h = '1080'
        _str_output_path = os.path.join(_path,_dir,_src_image)
        self.assertEqual(['ffmpeg',
                          '-i',_str_src_path,
                          '-pix_fmt','yuvj420p',
                          '-vf',_str_vf,
                          '-q:v','2',
                          _str_output_path],
             make_str_list_cmd_resize_images(_path,_dir,_src_image,_out_w,_out_h))


if __name__ == '__main__':
    #create_test_env()
    unittest.main()
    #clean_test_env()
