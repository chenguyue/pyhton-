import os
import random
import gzip
import urllib.request
import logging
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from os import path as osp

chapter_list = []
#获取章节列表
def get_chapter_list(url):
    browser = webdriver.PhantomJS()
    browser.get(url)
    chapter_elem_list = browser.find_elements_by_css_selector('body > div.wrap > div.middleright > div:nth-child(1) > div.cartoon_online_border > ul > li > a')
    for chapter_elem in chapter_elem_list:
        chapter_list.append((chapter_elem.get_attribute('title'),chapter_elem.get_attribute('href')))
    browser.quit()
    print(chapter_list)
#下载单一图片
def download_picture(url,save_path):
    req_html = urllib.request.Request(url=url,headers = headers)
    with open(save_path,'wb') as fp:
        fp.write(urllib.request.urlopen(req_html).read())
#下载某一章节
def download_chapter(chapter_idx):
    #chapter_list中是多个二元组的集合，如['第180话','具体url']
    #image_list中是一章漫画的每一页具体内容
    chapter = chapter_list[chapter_idx]
    chapter_title = chapter[0]
    chapter_url = chapter[1]
    image_list = []
    save_folder = 'D:/python/python_code/download_manhua/kanonair/'
    if not osp.exists(save_folder):
        os.mkdir(save_folder)
    save_folder = os.path.join(save_folder,chapter_title)
    if not osp.exists(save_folder):
        os.mkdir(save_folder)
        
    for key,value in enumerate(headers):
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value


    browser = webdriver.PhantomJS()
    browser.get(chapter_url)
    html = browser.page_source
    p_a = html.find('g_max_pic_count') + 18
    p_b = html.find(';',p_a)
    page_num = html[p_a:p_b]
    page_num = int(page_num)


    for n in range(0,page_num):        
        tag_image = browser.find_element_by_css_selector('#center_box > img')
        image_url = tag_image.get_attribute('src')
        image_name = tag_image.get_attribute('name')
        save_image_name = os.path.join(save_folder,('%05d' % n) + '.' + osp.basename(image_url).split('.')[-1])
        print(image_url)
        print(str(n) + '下载开始')
        download_picture(image_url,save_image_name)
        print(str(n) + '下载完成')
        if(n < page_num - 1):
            browser.find_element_by_css_selector('#center_box > a.img_land_next').click()
    browser.quit()


def start(url):
    begin = 0
    if len(chapter_list) >= 0:
        end = len(chapter_list)
    else:
        end = -1
    for chapter_idx in range(begin,end):
        download_chapter(chapter_idx)
    
if __name__ == '__main__':
    url = 'http://manhua.dmzj.com/kanonair/'
    headers = {
    "Host":"images.dmzj.com",
    "method":"GET",
    "Connection": "keep-alive",
    "Accept": "image/webp,image/*,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
    "Referer": "http://manhua.dmzj.com",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "scheme":"https",
    "authority":"images.dmzj.com",
    "Cookie":"show_tip_1=0; Hm_lvt_645dcc265dc58142b6dbfea748247f02=1488012060; Hm_lpvt_645dcc265dc58142b6dbfea748247f02=1488012300"
    }
    get_chapter_list(url)
    start(url)
