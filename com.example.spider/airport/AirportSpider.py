import os
import time
import urllib.request

import xlwt
from lxml import etree

'''
获取机场信息----探索版1
'''

def str_format(str):
    if str.find(',') == 0:
        return str.replace('\t', '').replace('\n', '').replace('\r', '')[1:]
    else:
        return str.replace('\t', '').replace('\n', '').replace('\r', '')


text = 'http://airport.anseo.cn/'
selector = etree.parse('http://airport.anseo.cn/', etree.HTMLParser())
html = selector.xpath('//*[@id="regions-list-c"]/div')

# 存储每个国家的url
list = []
# 表头
table_head = ['洲', '国家', '城市_中文名', '城市_英文名', '机场_中文名', '机场_英文名', '机场三字码', '机场四字码']
# 工作簿
book = xlwt.Workbook()
# 工作表
sheet = book.add_sheet('airport')
# 行数
row = 0
for item in range(len(table_head)):
    sheet.write(row, item, table_head[item])

# 遍历每个洲标签下的国家
for continent in html:
    # 获取洲名
    continent_name = continent.attrib['id']

    # print(state[0][0][0].text)
    for country in continent[0]:
        # 获取各洲下的国家名
        country_name = country[0].text
        # print(country[0].text)
        # 获取各州下国家的url
        country_url = 'http://airport.anseo.cn' + country[0].attrib['href']
        list.append({'continent': continent_name, 'country': country_name, 'url': country_url})
        # print(country_url)
        # 向各个国家发起请求，获取页面数据

# 解析每个国家的url
for ele in list:
    # 先解析一次，获取到页码
    first_parse = etree.parse(ele['url'], etree.HTMLParser())
    if ele['country'] == '中国澳门(Macau)':
        row += 1
        airport_zh = '澳门国际机场'
        airport_en = 'Macau International Airport'
        city_zh = '澳门'
        city_en = 'Macau'
        code_3 = 'MFM'
        code_4 = 'VMMC'
        column_data = [ele['continent'], ele['country'], city_zh, city_en, airport_zh, airport_en, code_3, code_4]
        for item in range(len(column_data)):
            sheet.write(row, item, column_data[item])

        print('写入：' + str(column_data))
    else:
        page_li = first_parse.xpath('/html/body/div[2]/div/div[2]/div/div[1]/div/div[2]/div/ul/li')
        page_list = []
        # 获取每个国家的总页码数
        if len(page_li) != 0:
            # 判断最后一个按钮是否是最后一页按钮：超过4页的才有
            # 是最后一页按钮的，页码为1到最后一页
            # 不是最后一页按钮的，页码为1到下一页按钮的前一个按钮的页码
            # last_button = int(page_li[-1][0].attrib['href'].split('-')[-1])
            last_button = page_li[-1][0]
            last_page = 0
            if last_button.text == '>>':
                last_page = int(page_li[-1][0].attrib['href'].split('-')[-1])
            else:
                last_page = int(page_li[-2][0].attrib['href'].split('-')[-1])
            # 将页码加入页码列表
            for i in range(1, last_page + 1):
                page_list.append(i)


        for page_num in page_list:
            time.sleep(1)
            # 根据每个国家的url解析到机场列表，etree格式
            # AirportSelector_exist_br = etree.parse(ele['url'] + '__page-' + str(page_num), etree.HTMLParser())
            AirportSelector_exist_br = urllib.request.urlopen(ele['url'] + '__page-' + str(page_num))
            # 因为直接解析的列表中存在不可解析的br，所以这里要先替换掉页面中的br标签，再解析一次
            AirportSelector_nonExist_br = etree.HTML(
                # etree.tostring(AirportSelector_exist_br).decode().replace('<br/>', ','))
                str(AirportSelector_exist_br.read().decode().replace('<br />', ',')))
            # page_html = AirportSelector_nonExist_br.xpath('/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]/table/tbody/tr')

            # 利用xpath定位到每个表格的行
            airport_html = AirportSelector_nonExist_br.xpath(
                '/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]/table/tbody/tr')
            # 遍历每一行，读取表格元素
            for td in airport_html:
                # 城市
                city_temp = td[0][0].text
                city = str_format(city_temp if city_temp is not None else '').split(',')
                # 机场名称
                airport_temp = td[1][0].text
                airport = str_format(airport_temp if airport_temp is not None else '').split(',')
                # 机场三字码
                code_3_temp = td[2][0][0].text
                code_3 = str_format(code_3_temp if code_3_temp is not None else '')
                # 机场四字码
                code_4_temp = td[3][0][0].text
                code_4 = str_format(code_4_temp if code_4_temp is not None else '')
                column_data = [ele['continent'], ele['country'], city[0], city[1], airport[0], airport[1], code_3,
                               code_4]
                row += 1
                for item in range(len(column_data)):
                    sheet.write(row, item, column_data[item])
                print('写入：' + str(column_data))

db_folder = 'd:/python'
if not os.path.exists('d:/python'):
    os.makedirs('d:/python')

xls_path = os.path.join(db_folder, "机场信息.xls")
book.save(xls_path)
