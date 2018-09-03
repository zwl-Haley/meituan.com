# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html




import pymysql
import datetime

class MeituanPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = "127.0.0.1",
            port = 3306,
            db = "meituan",
            user = "root",
            passwd = "",
            charset = 'utf8',
            use_unicode = True
            )
        self.cursor = self.connect.cursor()
    print("连接数据库成功，正在存入数据库...")

    def process_item(self, item, spider):
        self.cursor.execute(
            """replace into meishi(create_time, title, phone, city, shop_id)
            value (%s, %s, %s, %s, %s)""",
            (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            item["title"],
            item["phone"],
            item["city"],
            item["shop_id"]
             ))
        self.connect.commit()
        return item

    def close_spider(self,spider):
        self.connect.close()


# CREATE TABLE meishi (
#     auto_id INT NOT NULL primary key AUTO_INCREMENT,
#     create_time DateTime NOT NULL,
#     title VARCHAR(100),
#     phone VARCHAR(50),
#     city VARCHAR(20),
#     shop_id VARCHAR(50));