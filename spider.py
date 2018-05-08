#!usr/bin/python3
# _*_ coding:utf-8 _*_
# author: JemmyH
"""
爬取网站：http://www.5857.com
实现的功能：1. 将该网站上的所有照片按照所属类别、类别里面再使用标题建立目录，层次结构清晰
           2. 进行了一些异常处理，保证程序在网络状况良好的情况下不会中断
           3. 即使终端，可以快速启动并回到上次中断的地方（我使用了判断是否存在本地文件、如果存在则跳过的解决办法）
这段代码存在的问题：1. 没有设置request.urlopen()的timeout，这会导致程序在网络状况不好时出现“假死”现象（更新了）
                  2. 没有使用多线程操作。爬虫属于I/O密集型操作，这就导致大量的时间用来进行I/O操作，其实
              我们完全可以在某一个线程进行I/O操作的时候启动另一个进程进行网址解析等操作节约时间。（我写这段文字的时候刚学到多线程的概念，而程序已经在运行了）（已经进行了改进）
                  3. 没有使用回调函数（因为我还没学懂就没敢用），导致有几个函数代码块出现了代码重复（冗余），而且程序多使用循环，使程序的时间复杂度增大
                  4. 等想到了再更新

最新更新：1. 设置了timeout
         2. 使用了多线程并发处理
"""


import urllib.request
from lxml import etree
import os
import threading


def download_image(img_url, path):
    try:
        print(path)
        if os.path.exists(path):
            pass  # 如果该文件存在，则跳过执行保存操作，这方便中断爬虫之后再重新启动
        else:
            urllib.request.urlretrieve(img_url, path)  # 根据传进来的url下载图片并保存在设定的文件夹中
    except Exception as e:
        pass  # 出现某个错误或异常则跳过，不影响整个程序的继续运行


def get_html(content_url, dir_name, path, count):
    print(content_url)
    print(dir_name)
    path_ = path + dir_name
    if os.path.exists(path_):
        pass
    else:
        os.mkdir(path_)  # 创建本地文件
    try:
        html_ = urllib.request.urlopen(content_url).read().decode("utf-8")
        et_ = etree.HTML(html_)
        img_num_list = et_.xpath("/html/body/div[4]/div[2]/div[3]/div//a/text()")
    except Exception:
        pass
    try:
        img_num = int(img_num_list[len(img_num_list) - 2])  # 获取每个主题有多少张图片
    except Exception as e:
        img_num = 2
    for index in range(1, img_num):
        img_content_url = et_.xpath("/html/body/div[4]/div[2]/div[3]/a/img/@src")[0]
        if index < 10:
            name = "00" + str(index)
        else:
            name = "0" + str(index)
        img_url = img_content_url[:len(img_content_url)-7] + name + ".jpg"
        path = path_ + "\\{0}.jpg".format(name)  # 给每个主题的每张图片以数字命名
        download_image(img_url, path)
    print("第{0}项：{1}下载完成".format(count, path[12:len(path) - 8]))


def index_page(start_url, path):
    page_html = urllib.request.urlopen(start_url).read().decode("utf-8")  # 获取主页的html结构文件
    et = etree.HTML(page_html)  # 将html文件变成etree对象
    gotten_url = et.xpath("/html/body/div[4]/div[2]/ul/li//a/@href")  # 获取想要的结构中的href链接，但是还混合有别的，因此下面要清理一下
    desc_word = et.xpath("/html/body/div[4]/div[2]/ul/li//a/img/@alt")  # 获取每一个页面的描述文字，我这里直接获取到用于创建文件夹
    content_url = []  # 存放真正想爬取的url
    for i in range(0, len(gotten_url), 4):
        content_url.append(gotten_url[i])
    count = 0
    for j in range(0, len(desc_word)):
        count += 1
        get_html(content_url[j], desc_word[j], path, count)


def item(index_url, item_name):
    path = "F:\image\\" + item_name
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    index_html = urllib.request.urlopen(index_url).read().decode("utf-8")
    index_et = etree.HTML(index_html)
    index_num = int(index_et.xpath("/html/body/div[4]/div[2]/div[2]//a/text()")[-2])  # 获取总共有多少页
    index_urls = []
    for index in range(2, index_num + 1):
        index_urls.append(index_url + "index_" + str(index) + ".html")
    index_urls.insert(0, index_url)  # 获取所有页面的url
    for index in index_urls:
        index_page(index, path + "\\")


def main():
    url = "http://www.5857.com/"
    html = urllib.request.urlopen(url).read().decode("utf-8")
    et = etree.HTML(html)
    items = et.xpath("/html/body/div[2]/div[2]/div[1]/ul/li//a/text()")[1:]
    item_url = et.xpath("/html/body/div[2]/div[2]/div[1]/ul/li//a/@href")[1:]
    th = []
    for j in range(0, len(items)):
        th.append("t" + str(j))
    for i in range(6, len(items)):
        th[i] = threading.Thread(target=item, args=(item_url[i], items[i]))  # 创建多个线程
        th[i].start()  # 多个线程同时启动


if __name__ == '__main__':
    main()

