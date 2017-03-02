import os
import random
import gzip
import urllib.request
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from os import path as osp
chapter_list = []
#获取章节列表
def get_chapter_list(url):
    browser = webdriver.PhantomJS()
    browser.get(url)
    chapter_elem_list = browser.find_elements_by_css_selector('#play_0 ul li a')
    chapter_elem_list.reverse()
    
    for chapter_elem in chapter_elem_list:
        chapter_list.append((chapter_elem.text,chapter_elem.get_attribute('href')))
    browser.quit()
    print(chapter_list)

#下载单一图片
def download_picture(url,save_path):
    with open(save_path,'wb') as fp:
        fp.write(urllib.request.urlopen(url).read())
#下载单一章节
def download_chapter(chapter_idx):
    #chapter_list中是多个二元组的集合，如['第180话','具体url']
    chapter = chapter_list[chapter_idx]
    chapter_title = chapter[0]
    chapter_url = chapter[1]
    print('#### download chapter ' + chapter_title +' begin ####')
    save_folder = 'D:/python/python_code/download_manhua'
    save_folder = os.path.join(save_folder,chapter_title)
    if not osp.exists(save_folder):
        os.mkdir(save_folder)
    image_idx = 1
    browser = webdriver.PhantomJS()
    browser.get(chapter_url)
    while(True):
        image_url = browser.find_element_by_css_selector('#qTcms_pic').get_attribute('src')
        save_image_name = os.path.join(save_folder,('%05d' % image_idx) + '.' + osp.basename(image_url).split('.')[-1])
        download_picture(image_url,save_image_name)
        browser.find_element_by_css_selector('a.next').click()
        try:
            browser.find_element_by_css_selector('#bgDiv')
            break
        except NoSuchElementException:
            image_idx += 1
    browser.quit()
    print('#### download chapter ' + chapter_title +' complete ####')

def start():
    begin = 0
    if len(chapter_list) >= 0:
        end = len(chapter_list)
    else:
        end = -1
    print(chapter_list[begin])
    print(chapter_list[end-1])
    for chapter_idx in range(begin,end):
        download_chapter(chapter_idx)

if __name__ == '__main__':
    url = 'http://www.tazhe.com/mh/27245/'
    get_chapter_list(url)
    start()
