#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-06-09 13:42:49
# Project: mainpage

from pyspider.libs.base_handler import *
import MySQLdb

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://maoyan.com/', fetch_type='js', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        info = []
        index = 0
        for each in response.doc('.slick-track a').items():
            if index > 2:
                break
            item = {}
            url = each.attr('href')
            text = each.attr('data-bgurl')
            if text is None:
                text = each.attr('style')
                tmp = text.split('url(')
                tmp = tmp[1].split(')')
                text = tmp[0]
            item['id'] = index
            item['image_url'] = text
            item['detail_url'] = url
            info.append(item)
            index += 1

        db = MySQLdb.connect('localhost', 'root', 'hu13580503105', 'film_db', charset='utf8')
        cursor = db.cursor()

        cursor.execute('SELECT * FROM slick')
        count = cursor.rowcount
        if count is 3:
            sql = "DELETE FROM slick WHERE id > '%d'" % (-1)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        for item in info:
            sql = 'INSERT INTO slick(id, image_url, detail_url) VALUES ("%d", "%s", "%s")' % (item['id'], item['image_url'], item['detail_url'])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

        db.close()
