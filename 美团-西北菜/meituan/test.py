# -*- coding: utf-8 -*-
import requests
import re

# r = requests.get("http://www.meituan.com/changecity/",headers={"User-Agent":"Mozilla/5.0"})
# id_ = re.findall(r'"id":(\d+)',r.text)
# print(list(set(id_)))

url = "https://apimobile.meituan.com/group/v1/poi/177763452"
r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
print(r.text)
phone = re.findall(r'"phone":"([0-9-]+)"',r.text)[0]
print(phone)
