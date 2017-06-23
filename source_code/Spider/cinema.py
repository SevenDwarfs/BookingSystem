#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-06-05 13:13:53
# Project: cinema

from pyspider.libs.base_handler import *
import json
import os
import MySQLdb
import re
import time
import datetime

city_item = {'gz': '广州'}

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'cache-control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'mtcdn=K; lsu=; abt=1496711342.0%7CBDF; rvct=20%2C139%2C1; _lxsdk_s=5c952aa49ee9e4a6da62508b0450%7C%7C0; _lx_utm=; ci=175; ppos=44.582852%2C129.62047; pposn=%E9%9B%AA%E5%A8%83%E5%86%B0%E7%82%B9%E5%9F%8E; __mta=87815847.1496486340509.1496735867927.1496735876700.12; uuid=458263dd41694e0f8f21.1491469309.2.0.1; oc=TAUkz3SV8Zz2LYb5xM9kPHVvVnOgX8YCoMaKQL-zNJ4_Nld645qT6UdsjlQlD4tWBTfGEyGsCieA8xodNqfEXZJZgCqDNSv-7sBVxI0lxax2eXLz6Y237gnLmzI-8XxDNjwMrYg_Iml_1k6ZIQiiGHiMit3YXC5sAiRNkNCqqQc; __utma=211559370.898660114.1492826996.1496711380.1496733025.9; __utmb=211559370.15.9.1496734397925; __utmc=211559370; __utmz=211559370.1492826996.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=211559370.|1=city=mdj=1',
            'Host':'gz.meituan.com',
            # 'Referer':'http://gz.meituan.com/dianying/cinemalist?mtt=1.movie%2Fmoviedeal.0.0.j3kvaygr',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36',
            # 'X-Requested-With':'XMLHttpRequest',
        }

    @every(minutes=24 * 60)
    def on_start(self):
        for item in city_item:
            url = 'http://'+item+'.meituan.com/dianying/cinemalist/all/all/page1'
            self.crawl(url, fetch_type='js', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        url = response.url
        tmp = url.split('page')
        page_index = int(tmp[1])
        string = (url.split('.'))[0]
        tmp = string.split('//')
        city = city_item[tmp[1]]
        for each in response.doc('.cinema-item__block h4 a').items():
            self.crawl(each.attr.href, fetch_type='js', headers=self.header, callback=self.detail_page, save={'city': city})
        url = response.doc('.next a').attr('href')
        # if url and page_index < 4:
        self.crawl(url, fetch_type='js', callback=self.index_page)
        # self.crawl('http://gz.meituan.com/shop/1436366', fetch_type='js', headers=self.header, callback=self.detail_page, save={'city': '广州'})


    @config(priority=2)
    def detail_page(self, response):
        cinema_info = {}
        cinema_info['city'] = response.save['city']
        cinema_info['cinema_name'] = response.doc('.biz-name').text().strip(' ').strip('查看其他分店').strip(' ')
        # rating = response.doc('.biz-level').text()
        # tmp = rating.split(' ')
        # rating = ''.join(tmp)
        # cinema_info['rating'] = rating
        for index, item in enumerate(response.doc('.field-group').items()):
            if index is 0:
                tmp = item.text().split('：')
                address = tmp[1].strip(' ').split('\n')
                cinema_info['address'] = ' '.join(address)
                # cinema_info['block'] = place[0]
                # tmp1 = place[1].strip(' ').split(' ')
                # cinema_info['address'] = tmp1[0]
            if index is 1:
                tmp = item.text().split('：')
                cinema_info['phone'] = tmp[1].strip(' ')
            # if index is 2:
            #     tmp = item.text().split('：')
            #     cinema_info['cinema_service'] = tmp[1].strip(' ')
            # if index is 4:
            #     tmp = item.text().split('：')
            #     cinema_info['shop_service'] = tmp[1].strip(' ')
            # if index is 5:
            #     tmp = item.text().split('：')
            #     cinema_info['introduction'] = tmp[1].strip(' ')

        screen_info = []
        for item in response.doc('.movie-info').items():
            movie_name = item.children('header a h3').text()
            date = []
            for date_item in item.children('.show-time a').items():
                string = date_item.text().strip('）')
                tmp = string.split('（')
                if len(tmp) > 1:
                    string = tmp[1]
                string = (string.split('周'))[0]
                tmp = string.split('.')
                date_item = datetime.date(int('2017'), int(tmp[0]), int(tmp[1]))
                date_item.strftime('%Y-%m-%d')
                date.append(date_item)

            for time_index, time_item in enumerate(item.children('.time-table').items()):
                for row_index, row_item in enumerate(time_item.children('tbody tr').items()):
                    if row_index != 0:
                        info = {}
                        info['movie_name'] = movie_name
                        info['date'] = date[time_index]
                        flag = 1
                        for col_index, col_item in enumerate(row_item.children('td').items()):
                            if col_index is 0:
                                tmp = col_item.text().split('−')
                                if len(tmp) < 2:
                                    flag = 0
                                    break
                                tmp[0] = tmp[0].strip(' ')
                                tmp[1] = tmp[1].strip(' ')
                                info['time'] = '−'.join(tmp)
                            if col_index is 1:
                                info['language'] = col_item.text().strip(' ')
                            if col_index is 2:
                                info['room'] = col_item.text().strip(' ')
                            if col_index is 3:
                                string = col_item.text().strip(' ')
                                if string is '暂无价格信息':
                                    info['price'] = 60
                                else:
                                    tmp = string.split('¥')
                                    if len(tmp) is 1:
                                        info['price'] = 60
                                    else:
                                        if string.find('扫描二维码下载猫眼电影手机版享受手机特惠') == -1:
                                            string = tmp[1].strip(' ')
                                            tmp = string.split(' ')
                                            info['price'] = float(tmp[0].strip('元'))
                                        else:
                                            info['price'] = 60
                        if flag == 1:
                            screen_info.append(info)

        db = MySQLdb.connect('localhost', 'root', 'hu13580503105', 'film_db', charset='utf8')
        cursor = db.cursor()

        cursor.execute('SELECT id FROM cinema WHERE name="%s"' % cinema_info['cinema_name'])
        count = cursor.rowcount
        if count is 0:
            cursor.execute('SELECT * FROM cinema')
            cinemaid = cursor.rowcount
            sql = 'INSERT INTO cinema (id, name, address, phone, city) VALUES ("%d", "%s", "%s", "%s", "%s")' % (cinemaid, cinema_info['cinema_name'], cinema_info['address'], cinema_info['phone'], cinema_info['city'])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            cursor.execute('SELECT * FROM screen')
            screenid = cursor.rowcount
            for item in screen_info:
                sql = 'INSERT INTO screen (id, language, price, room, show_date, show_time, cinema_id, movie_name) VALUES ("%d", "%s", "%f", "%s", "%s", "%s", "%d", "%s")' % (screenid, item['language'], item['price'], item['room'], item['date'], item['time'], cinemaid, item['movie_name'])
                try:
                    screenid += 1
                    cursor.execute(sql)
                    db.commit()
                except:
                    screenid -= 1
                    db.rollback()

        db.close()
