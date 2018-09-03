# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import re
from jiudian.cityList import cityList
from jiudian.items import JiudianItem

class JdSpider(scrapy.Spider):
    name = 'jd'
    def __init__(self, city=None, *args, **kwargs):
        super(JdSpider, self).__init__(*args, **kwargs)
        self.cityName = city
        self.cityId = re.findall(r"\(\'(\d+)\', \'{}\'\)".format(city),str(cityList))[0]
        self.startDay =  datetime.date.today()
        self.endDay = self.startDay + datetime.timedelta(days=1)

    def start_requests(self):
        offset = 0
        startDay = self.startDay.strftime("%Y%m%d")
        endDay = self.endDay.strftime("%Y%m%d")
        cityId = self.cityId
        while offset < 2021:
            start_url = "https://ihotel.meituan.com/hbsearch/HotelSearch?newcate=1&cateId=20&userid=985749111&uuid=17E0D702C912FCE691CD0DCB4908B901A1B8FF7216C24209380605324EC1F22F&attr_28=129&limit=20&offset={}&cityId={}&sort=defaults&endDay={}&startDay={}&sourceType=hotel&client=iphone&utm_medium=WEIXINPROGRAM&utm_term=8.7.0&version_name=8.7.0&utm_campaign=entry=MTLive_scene=1089".format(offset,str(cityId),endDay,startDay)
            offset += 20
            yield scrapy.Request(start_url)

    def parse(self, response):

        text = response.text
        res_json = json.loads(text)
        data_list = res_json["data"]["searchresult"]
        for data in data_list:
            #酒店名称
            title = data["name"]
            #poiid为酒店id，这里查找电话要用
            poiid = data["poiid"]
            #地址
            addr = data["addr"]
            #最低价格
            lowestPrice = data["lowestPrice"]


            phone_url = "https://ihotel.meituan.com/group/v1/poi/{}?_token=&start=1531526400000&end=1531612800000&cityId=1&subtype=0&type=1&isRecommend=0&recType=0&isLocal=1&entryType=2&utm_medium=WEIXINPROGRAM&fields=phone,name&utm_term=8.7.0&version_name=8.7.0".format(poiid)
            yield scrapy.Request(phone_url, callback=self.parse_phone,dont_filter=False, meta={"title":title,"addr":addr,"lowestPrice":lowestPrice,"poiid":poiid})

    def parse_phone(self, response):
        item = JiudianItem()
        res_json = json.loads(response.text)

        item["title"] = response.meta["title"]
        item["addr"] = response.meta["addr"]
        item["lowestPrice"] = response.meta["lowestPrice"]
        #区域
        item["quyu"] = response.meta["addr"].split("区")[0] + "区"
        item["phone"] = res_json["data"][0]["phone"]
        item["poiid"] = response.meta["poiid"]
        item["cityName"] = self.cityName

        yield item
