# -*- coding: utf-8 -*-
import scrapy
import re
import json
# import requests
from meituan.cityList import cityList
from meituan.items import MeituanItem


class MtSpider(scrapy.Spider):
    name = 'mt'

    def start_requests(self):
        key_words = ["陕西风味面馆", "陕西风味小吃", "肉夹馍", "凉皮", "米皮", "擀面皮", "油泼面", "臊子面", "泡馍", "冰峰", "稠酒"]
        for city_id in cityList:
            for key_word in key_words:
                url = "http://api.meituan.com/group/v2/poi/search/{}?q={}&cateId=1&sort=defaults&client=android&offset=0".format(city_id[0], key_word)
                yield scrapy.Request(url,meta={"city":city_id[1]})

    def parse(self, response):
        totalCount = re.findall(r'"totalcount":(\d+),',response.text)[0]
        print("搜索到店铺数量：",totalCount)
        if not totalCount == '0':
            max_page = int((int(totalCount)+14)/15)
            for page in range(0, max_page+16, 15):
                url = response.url.replace("offset=0","offset={}".format(str(page)))
                yield scrapy.Request(url, callback=self.parse_shop, meta={"city":response.meta["city"]})

    def parse_shop(self, response):
        item = MeituanItem()
        try:
            res_json = json.loads(response.text)
            result_list = res_json["data"]["searchresult"]
            for result in result_list:
                shop_id = result["poiid"]
                title = result["name"]
                city = response.meta["city"]
                phone = result["phone"]

                item["shop_id"] = shop_id
                item["title"] = title
                item["city"] = city
                item["phone"] = phone
                yield item
        except:
            print("返回内容无数据，内容为：",response.text)

    # def get_phone(self, shop_id):
    #     url = "https://apimobile.meituan.com/group/v1/poi/{}".format(shop_id)
    #     r = requests.get(url, headers={"User-Agent":"Mozilla/5.0", "Connection": "close"})
    #     phone = re.findall(r'"phone":"([0-9-]+)"',r.text)
    #     return phone[0] if phone else ""
