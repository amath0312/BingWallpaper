#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#import sys, io
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

import sys,os,logging,time,datetime
if os.name == 'nt':
    import win32api, win32gui, win32api, win32con
logging.basicConfig(level=logging.INFO)


from BingWallPaper import WallPaper

def setUbuntuWallPaper(imagepath):
    fileuri = 'file://%s'%imagepath
    command = 'gsettings set org.gnome.desktop.background picture-uri %s' % fileuri
    os.system(command)
    print("backimage: ", imagepath)

def setWindowsWallPaper(imagepath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,imagepath, 1+2)
    print("backimage: ", imagepath)

def setWallPaper(imagepath):   
    if os.name == 'posix':
        setUbuntuWallPaper(imagepath)
    elif os.name == 'nt':
        setWindowsWallPaper(imagepath)

def isNext(oper):
    return oper == 'n' or oper == 'N'

def isPrev(oper):
    return oper == 'p' or oper == 'P'

def isQuit(oper):
    return oper == 'q' or oper == 'Q'


def handleWallPaper(wallpaper):
    oper = ''
    tips = '''
    n: next image
    p: previous image
    q: quit
    '''
    while not isQuit(oper):
        oper = input(tips)
        if isNext(oper):
            setWallPaper(wallpaper.next())
        elif isPrev(oper):
            setWallPaper(wallpaper.previous())
        elif isQuit(oper):
            break


if __name__ == '__main__':
    auto = False
    if len(sys.argv) > 1:
        auto = sys.argv[1] == 'auto'

    today = datetime.date.today()
    logging.info('is auto set?%s' % auto)
    
    if os.name == 'nt':
       root = 'c:\\bing\\WallPaper'
    elif os.name == 'posix':
        root = '/home/zhaolin/bing'

    bg_path = ('%s%s%04d%02d%02d%s' % (root, os.sep, today.year,today.month,today.day, os.sep))
    wallpaper = WallPaper(bg_path,clear_old_wallpapers=False)
    if not wallpaper.get_wallpapers():
        logging.error('download wallpapers error, exit')
        os._exit(0)

    if auto:
        path = wallpaper.random()
        setWallPaper(path)
    else:
        handleWallPaper(wallpaper=wallpaper)
