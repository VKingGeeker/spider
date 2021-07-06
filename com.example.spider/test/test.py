import math
import urllib.request
from re import split

from lxml import etree

# response = urllib.request.urlopen('http://airport.anseo.cn/c-china')
# #
# #
# print(response.read())
from lxml.doctestcompare import strip

# res = etree.HTML('<a href="#" title="Beijing" target="_blank">\n\t\t\t\t\t\t\t\t\t&#21271;&#20140;\t\t\t\t\t\t\t\t\t<br/>\n\t\t\t\t\t\t\t\t\tBeijing\t\t\t\t\t\t\t\t\t</a>'.replace('<br/>',','))
#
# print(strip(res[0][0].text.split(',')[1]))
def str_format(str):
    if str.find(',') == 0:
        return str.replace('\t', '').replace('\n', '')[1:]
    else:
        return str.replace('\t', '').replace('\n', '')

# AirportSelector_exist_br = etree.parse('http://airport.anseo.cn/c-china', etree.HTMLParser())
AirportSelector_exist_br = urllib.request.urlopen('http://airport.anseo.cn/c-china')
node = etree.HTML(AirportSelector_exist_br.read())
# print(etree.tostring(AirportSelector_exist_br).decode())
# text = node.xpath('/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]/table/thead')
# print(text[0][0][0].text)
# text_arr = text[0].split(' ')
# mac_zh=text_arr[0]
# mac_en=text_arr[1]+text_arr[2]+text_arr[3]
# print(mac_en)


# str = ''
# print(str_format(str))
# print(str.find(','))


AirportSelector_exist_br = urllib.request.urlopen('http://airport.anseo.cn/c-china')
str=AirportSelector_exist_br.read().decode().replace('<br />', ',')
# print(str)
# 因为直接解析的列表中存在不可解析的br，所以这里要先替换掉页面中的br标签，再解析一次
AirportSelector_nonExist_br = etree.HTML(
    # etree.tostring(AirportSelector_exist_br).decode().replace('<br/>', ','))
    str
    # AirportSelector_exist_br.read()
)

# page_li = AirportSelector_nonExist_br.xpath('/html/body/div[2]/div/div[2]/div/div[1]/div/div[2]/div/ul/li')
#
# print(page_li[-1][0].text)

print(math.ceil(9 / 2))
# airport_html = AirportSelector_nonExist_br.xpath(
#     '/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]/table/tbody/tr')
#
# for td in airport_html:
#     # 城市
#     city_temp = td[0][0].text
#     city = str_format(city_temp if city_temp is not None else '').split(',')
#     # 机场名称
#     airport_temp = td[1][0].text
#     airport = str_format(airport_temp if airport_temp is not None else '').split(',')
#     # 机场三字码
#     code_3_temp = td[2][0][0].text
#     code_3 = str_format(code_3_temp if code_3_temp is not None else '')
#     # 机场四字码
#     code_4_temp = td[3][0][0].text
#     code_4 = str_format(code_4_temp if code_4_temp is not None else '')
#
#     colume_data = [city[0], city[1], airport[0], airport[1], code_3,
#                 code_4]
#
#     # print(td[1][0].t/ext)
#     print(city_temp)
