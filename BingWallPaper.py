# -*- coding:utf-8 -*-
import sys,os
import urllib.request
import time
import json
import random
import logging


class WallPaper(object):
    def __init__(self, bg_path='c:\\bing\\wallpaper\\', clear_old_wallpapers=True, max_cnt=10, try_times=20):
        self.total_cnt = max_cnt
        self.try_times = try_times
        self.clear_old_wallpapers=clear_old_wallpapers
        self.bg_path = bg_path
        self.bg_filename_pattern = os.path.join(bg_path, 'bg%d.jpg')
        self.url = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=%d&nc=%d&pid=hp&video=1" % (self.total_cnt, int(time.time()))
        self.img_url_prefix = 'http://cn.bing.com'
    def __get_wallpaper_info(self):
	    logging.info('get info from: %s' % self.url)

	    req = urllib.request.Request(url=self.url, headers={},method='GET')
	    resp = None
	    for try_time in range(self.try_times):
	        try:
	            resp = urllib.request.urlopen(req).read()
	        except Exception as e:
	            logging.warn('try ', try_time, ':', e)
	            resp = None
	        if resp:
	            break
	        else:
	            time.sleep(2)

	    if resp:
	        data = json.loads(resp.decode('utf-8'))
	        if data and data['images'] :
	            self.images = data['images']
	            return True

	    self.images = None
	    return False

    def __download_wallpaper(self):
        real_cnt = 0
        for idx, img in enumerate(self.images):
            filename = self.bg_filename_pattern % idx
            if os.path.exists(filename) and not self.clear_old_wallpapers:
                pass
            else:
                img_url = (img['url'])
                if not img_url.startswith('http'):
                    img_url = self.img_url_prefix+img_url
                logging.info('download %s from %s' % (filename, img_url))
                
                img_data = urllib.request.urlopen(img_url).read()
                logging.info('download %s success' % img_url)
                
                open(self.bg_filename_pattern % idx,'wb').write(img_data)
            real_cnt = real_cnt + 1
        self.total_cnt = real_cnt   

    def __clear_wallpaper_path(self):
        if not os.path.exists(self.bg_path):
            os.makedirs(self.bg_path)
        elif self.clear_old_wallpapers:
            files = os.listdir(self.bg_path)
            for f in os.scandir(self.bg_path):
                if f.is_file():
                    os.remove(f.path)

    def get_wallpapers(self):
        if not self.__get_wallpaper_info():
            return False

        self.__clear_wallpaper_path()
        self.__download_wallpaper()
        self.wallpaper_index = -1
        return True

    def next(self):
        idx = self.wallpaper_index + 1
        if idx >= self.total_cnt:
            idx = 0
        self.wallpaper_index = idx
        return self.bg_filename_pattern % self.wallpaper_index

    def previous(self):
        idx = self.wallpaper_index - 1
        if idx < 0:
            idx = self.total_cnt - 1
        self.wallpaper_index = idx
        return self.bg_filename_pattern % self.wallpaper_index

    def random(self):
        random.seed(int(time.time()))
        path = self.bg_filename_pattern % int(random.random() * self.total_cnt)
        return path