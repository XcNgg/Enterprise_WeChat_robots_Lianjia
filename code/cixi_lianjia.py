# encoding:utf-8
# !/usr/bin/python3
# @AUTHOR : XcNgg

import re
from bs4 import BeautifulSoup
import requests
from my_fake_useragent import UserAgent

# 爬虫类
class spider:
    # 初始化
    def __init__(self):
        self.headers={
            "User-Agent": UserAgent().random()
        }
        self.data_list = []

    #传参翻页
    def fetch_https(self,page):
        """
        :param page: 页码
        :return: 当前页数网站的响应状态
        """
        self.headers['Referer'] = 'https://nb.lianjia.com/'
        self.headers['User-Agent'] = UserAgent().random()
        url = f'https://nb.lianjia.com/zufang/cixishi/pg{page}rp2/#contentList'
        response = requests.get(url, headers=self.headers)
        return response
    # 解析器
    def parser(self,response):
        """
        :param response: 当前页数的响应状态
        :return:  当前页数的数据列表
        """
        soup = BeautifulSoup(response.text, 'lxml')
        item_list =soup.select('div[class="content__list"] div[class="content__list--item"]' )
        data_list = []
        for index,item in enumerate(item_list):
            data ={}
            main = item.select('div[class="content__list--item--main"]')[0]
            #解析标题
            title = main.select('p[class^="content__list--item--title"]')[0].text.replace('\n','').replace('\t','').replace(' ','')
            data['title'] = title
            #解析直达URL
            url = main.select('p[class^="content__list--item--title"] a')[0]['href']
            data['url'] = url
            #解析相关信息列表
            info =main.select('p[class="content__list--item--des"]')[0].text.replace('\n','').replace('\t','').replace(' ','')
            data['info_list'] = info.split('/')
            #解析租金价格
            price = main.select('span em')[0].text.replace('\n','').replace('\t','').replace(' ','')
            data['price'] = price
            # print(price)
            #解析图片地址
            img_src = item.select('a[class^="content__list--item--aside"] img')[0]['data-src']
            data['img_src'] = img_src
            # print(data)
            data_list.append(data)
        return data_list

    # 跑动入口
    def run(self,page):
        """
        :param page: 页码
        :return: None
        """
        response = self.fetch_https(page)
        self.data_list +=self.parser(response)


    """
        得到最大页数
    """
    def get_max_page(self):
        url = "https://nb.lianjia.com/zufang/cixishi/rp2/"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            result = re.findall('<div class="content__pg" data-el="page_navigation".*data-totalPage=(.*) data-curPage=1>',response.text)
            return int(result[0])


#
# #

if __name__ == "__main__":
    crawler = spider()
    max_page = crawler.get_max_page()
    for page in range(1,max_page+1):
        crawler.run(page)
    for d in crawler.data_list:
        print(d)
    print(len(crawler.data_list))



