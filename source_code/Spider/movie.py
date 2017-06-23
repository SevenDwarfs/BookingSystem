#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-04-19 21:08:28
# Project: maoyan

from pyspider.libs.base_handler import *
import json
import os
import time
import MySQLdb
import re
import time
import datetime

class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v223',
    }

    def __init__(self):
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'cache-control':'max-age=0',
            'Cookie':'_lxsdk=15b427e86df0-013da14baa8ae5-24414032-100200-15b427e86e0c8; __utma=17099173.1793184252.1492609870.1492609870.1492609870.1; __utmz=17099173.1492609870.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _lx_utm=; __mta=41653021.1491469240404.1496486523638.1496486534862.164; _lxsdk_s=02f55d53e9ed2594387964d3afb1%7C%7C76; lt=GZGYNzTTEA9xQ3yubJoT_m8yKC4AAAAAKAQAAMziXZo3J0DdZBE5D55vl-By0BTPBumYmHDoCSCW-8y123cXiC4qYTUfzXY0sZk8FA; lt.sig=PiC6DPxLrYQkAfLOVSAOQZwcyEk',
            # 'Host':'xueqiu.com',
            'Referer':'https://passport.meituan.com/account/unitivelogin?service=maoyan&continue=https%3A%2F%2Fmaoyan.com%2Fpassport%2Flogin%3Fredirect%3D%252Ffilms%253FshowType%253D1%2526offset%253D3000',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
        }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://maoyan.com/films?showType=1&offset=0', fetch_type='js', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.movie-list dd').items():
            string = '暂无评分'
            tip = each.children('.channel-detail-orange').text()
            if tip != '暂无评分':
                rating1 = each.children('.channel-detail-orange .integer').text()
                rating2 = each.children('.channel-detail-orange .fraction').text()
                string = rating1+rating2
            url = each.children('.movie-item a').attr('href')
            self.crawl(url, fetch_type='js', callback=self.detail_page, save={'rating':string})
        url = response.url
        offset = url.split('offset=')
        index = 0
        if len(offset) > 1:
            index = int(offset[1]) / 30 + 1
        if index < 15:
            nextpage = response.doc('.list-pager :last-child a').attr('href')
            self.crawl(nextpage, fetch_type='js', callback=self.index_page)


    @config(priority=2)
    def detail_page(self, response):
        db = MySQLdb.connect('localhost', 'root', 'hu13580503105', 'film_db', charset='utf8')
        cursor = db.cursor()
        info = {}
        info['chinese_name'] = response.doc('.movie-brief-container h3').text()
        info['english_name'] = response.doc('.movie-brief-container div').text()
        info['url'] = response.doc('.avater-shadow img').attr('src')
        info['rating'] = response.save['rating']

        for index, item in enumerate(response.doc('.movie-brief-container ul li').items()):
            string = item.text()
            if index is 0:
                tmp = string.split(',')
                info['type'] = tmp[0]
            if index is 1:
                tmp = string.split('/')
                info['country'] = tmp[0].strip(' ').strip('\n')
                if len(tmp) > 1:
                    info['length'] = tmp[1].strip(' ')
                else:
                    info['length'] = None
            if index is 2:
                searchObj = re.search(r'\d+-\d+-\d+', string)
                if searchObj:
                    date = searchObj.group()
                    info['release_date'] = date
                    string = string.strip(date)
                else:
                    info['release_date'] = None
                searchObj = re.search(r'\d+(-\d+)*', string)
                if searchObj:
                    string = string.strip(searchObj.group())
                info['show_place'] = string
        for index, item in enumerate(response.doc('.module').items()):
            if index is 0:
                info['introduction'] = item.children('.mod-content span').text()  #剧情
            if index is 1:
                for i, group in enumerate(item.children('.mod-content .celebrity-container .celebrity-group').items()):
                    if i is 0:
                        director = []
                        persontype = group.children('.celebrity-type').text()
                        if persontype == '导演':
                            for li in group.children('ul li').items():
                                item = {}
                                name = li.children('.info a').text()
                                item['name'] = name
                                url = li.children('a img').attr('data-src')
                                if url == None:
                                    url = li.children('a img').attr('src')
                                item['url'] = url
                                director.append(item)
                            info['director'] = director  #导演
                        else:
                            actor = []
                            for li in group.children('ul li').items():
                                item = {}
                                name = li.children('.info a').text()
                                item['name'] = name
                                url = li.children('a img').attr('data-src')
                                if url == None:
                                    url = li.children('a img').attr('src')
                                item['url'] = url
                                actor.append(item)
                            info['actor'] = actor #演员
                    if i is 1:
                        actor = []
                        for li in group.children('ul li').items():
                            item = {}
                            name = li.children('.info a').text()
                            item['name'] = name
                            url = li.children('a img').attr('data-src')
                            if url == None:
                                url = li.children('a img').attr('src')
                            item['url'] = url
                            actor.append(item)
                        info['actor'] = actor #演员
        album = []
        for item in response.doc('.tab-img img').items():
            album.append(item.attr('data-src'))
        print(len(album))
        if len(album) > 0:
            info['album'] = album

        cursor.execute('SELECT id FROM movie WHERE chinese_name="%s"' % info['chinese_name'])
        rowcount = cursor.rowcount
        if rowcount is 0:
            cursor.execute('SELECT * FROM movie')
            filmid = cursor.rowcount
            date = None
            if info['release_date'] != None:
                tmp = info['release_date'].split('-')
                date = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
                date.strftime('%Y-%m-%d')

            part1 = []
            part2 = []
            part3 = []
            part1.append('INSERT INTO movie (id, chinese_name')
            part2.append('VALUES ("%d", "%s"')
            part3.append(filmid)
            part3.append(info['chinese_name'])

            if info['english_name'] != '':
                part1.append(', english_name')
                part2.append(', "%s"')
                part3.append(info['english_name'])

            part1.append(', url, type')
            part2.append(', "%s", "%s"')
            part3.append(info['url'])
            part3.append(info['type'])

            if info['length'] != None:
                part1.append(', length')
                part2.append(', "%s"')
                part3.append(info['length'])

            if date != None:
                part1.append(', release_date')
                part2.append(', "%s"')
                part3.append(date)

            part1.append(', introduction, rating, country')
            part2.append(', "%s", "%s", "%s"')
            part3.append(info['introduction'])
            part3.append(info['rating'])
            part3.append(info['country'])

            if info['show_place'] != None:
                part1.append(', show_place')
                part2.append(', "%s"')
                part3.append(info['show_place'])

            part1.append(') ')
            part2.append(')')

            part1_string = ''.join(part1)
            part2_string = ''.join(part2)
            part3_tuple = tuple(part3)

            string = part1_string + part2_string
            sql = string % part3_tuple

            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            if 'director' in info:
                for i in range(len(info['director'])):
                    item = (info['director'])[i]
                    cursor.execute('SELECT id FROM person WHERE name="%s" AND type="导演"' % (item['name']))
                    rowcount = cursor.rowcount
                    directorid = -1
                    if rowcount != 0:
                        directorid = (cursor.fetchone())[0]
                    else:
                        cursor.execute('SELECT id FROM person')
                        directorid = cursor.rowcount
                        sql = 'INSERT INTO person(id, name, url, type) VALUES ("%d", "%s", "%s", "导演")' % (directorid, item['name'], item['url'])
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rollback()
                    sql = 'INSERT INTO movie_person(mid, pid) VALUES ("%d", "%d")' % (filmid, directorid)
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()

            if 'actor' in info:
                for i in range(len(info['actor'])):
                    item = (info['actor'])[i]
                    cursor.execute('SELECT id FROM person WHERE name="%s" AND type="演员"' % (item['name']))
                    rowcount = cursor.rowcount
                    actorid = -1
                    if rowcount != 0:
                        actorid = (cursor.fetchone())[0]
                    else:
                        cursor.execute('SELECT id FROM person')
                        actorid = cursor.rowcount
                        sql = 'INSERT INTO person(id, name, url, type) VALUES ("%d", "%s", "%s", "演员")' % (actorid, item['name'], item['url'])
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rollback()
                    sql = 'INSERT INTO movie_person(mid, pid) VALUES ("%d", "%d")' % (filmid, actorid)
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()

            if 'album' in info:
                for i in range(len(info['album'])):
                    item = (info['album'])[i]
                    print(item)
                    sql = 'INSERT INTO movie_picture(url, mid) VALUES ("%s", "%d")' % (item, filmid)
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()

        db.close()
