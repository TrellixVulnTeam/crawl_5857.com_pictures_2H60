#!usr/bin/python3
# _*_ coding:utf-8 _*_
# author: JemmyH

import urllib.request
from lxml import etree
import os


def download_image(img_url, path):
    print(path)
    urllib.request.urlretrieve(img_url, path)  # 根据传进来的url下载图片并保存在设定的文件夹中


def get_html(content_url, dir_name):
    print(content_url)
    print(dir_name)
    path = "F:\image\\" + dir_name
    os.mkdir(path)  # 创建本地文件
    html_ = urllib.request.urlopen(content_url).read().decode("utf-8")
    et_ = etree.HTML(html_)
    img_num_list = et_.xpath("/html/body/div[4]/div[2]/div[3]/div//a/text()")
    img_num = int(img_num_list[len(img_num_list) - 2])  # 获取每个主题有多少张图片
    for index in range(0, img_num):
        img_content_url = et_.xpath("/html/body/div[4]/div[2]/div[3]/a/img/@src")[0]
        img_url = img_content_url[:len(img_content_url)-7] + "00" + str(index+1) + ".jpg"
        path = "F:\image\\" + dir_name + "\\{0}.jpg".format(str(index+1))  # 给每个主题的每张图片以数字命名
        download_image(img_url, path)
    print("第{}item结束".format(str(index + 1)))  # 标记每个主题结束


if __name__ == '__main__':
    start_url = "http://www.5857.com/neiyi/"  #首先进去主页
    html = urllib.request.urlopen(start_url).read().decode("utf-8")  # 获取主页的html结构文件
    et = etree.HTML(html)  # 将html文件变成etree对象
    gotten_url = et.xpath("/html/body/div[4]/div[2]/ul/li//a/@href")  # 获取想要的结构中的href链接，但是还混合有别的，因此下面要清理一下
    desc_word = et.xpath("/html/body/div[4]/div[2]/ul/li//a/img/@alt")  # 获取每一个页面的描述文字，我这里直接获取到用于创建文件夹
    content_url = []  # 存放真正想爬取的url
    for i in range(0, len(gotten_url), 4):
        content_url.append(gotten_url[i])
    for j in range(0, len(desc_word)):
        get_html(content_url[j], desc_word[j])


