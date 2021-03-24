import os
import time
import urllib.request

import xlwt
from lxml import etree

'''
先访问每个国家机场列表一次，获取到每个国家的页码数，并生成url，保存到country_url.txt文件中
'''

text = 'http://airport.anseo.cn/'
selector = etree.parse('http://airport.anseo.cn/', etree.HTMLParser())
html = selector.xpath('//*[@id="regions-list-c"]/div')

# 存储每个国家的第一页的url
pagelist_1 = []
pagelist_2 = []

# 遍历每个洲标签下的国家，保存每个国家的首页url
for continent in html:
    # 获取洲名
    continent_name = continent.attrib['id']
    for country in continent[0]:
        # 获取各洲下的国家名
        country_name = country[0].text
        # 获取各州下国家的url
        country_url = 'http://airport.anseo.cn' + country[0].attrib['href']
        pagelist_1.append({'continent': continent_name, 'country': country_name, 'url': country_url})

# 访问每个国家第一页的页码数据，获取全部页码的url并保存到pagelist_2
for ele in pagelist_1:
    # 先解析一次，获取到页码
    first_parse = etree.parse(ele['url'], etree.HTMLParser())
    page_li = first_parse.xpath('/html/body/div[2]/div/div[2]/div/div[1]/div/div[2]/div/ul/li')
    page_list = []
    # 获取每个国家的总页码数
    if len(page_li) != 0:
        last_button = page_li[-1][0]
        last_page = 0
        if last_button.text == '>>':
            last_page = int(page_li[-1][0].attrib['href'].split('-')[-1])
        else:
            last_page = int(page_li[-2][0].attrib['href'].split('-')[-1])
            # 将页码加入页码列表
        for i in range(1, last_page + 1):
            pagelist_2.append(
                {'continent': ele['continent'], 'country': ele['country'], 'url': ele['url'] + '__page-' + str(i)})
    else:
        pagelist_2.append(
            {'continent': ele['continent'], 'country': ele['country'], 'url': ele['url']})
# 将国家对应的URL写入到文件
file_write_obj = open("d:/python/country_url.txt", 'w')
for ele in pagelist_2:
    file_write_obj.writelines(ele['continent'] + ',' + ele['country'] + ',' + ele['url'])
    file_write_obj.write('\n')
file_write_obj.close()
