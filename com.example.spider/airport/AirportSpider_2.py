import os
import time
import urllib.request

import xlwt
from lxml import etree

'''
获取机场信息----探索版2
'''

def str_format(str):
    if str.find(',') == 0:
        return str.replace('\t', '').replace('\n', '').replace('\r', '')[1:]
    else:
        return str.replace('\t', '').replace('\n', '').replace('\r', '')


text = 'http://airport.anseo.cn/'
selector = etree.parse('http://airport.anseo.cn/', etree.HTMLParser())
html = selector.xpath('//*[@id="regions-list-c"]/div')

# 存储每个国家的第一页的url
pagelist_1 = []
pagelist_2 = []
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

# 循环全部url，每个url是一个分页，加入数据到excel
for ele in pagelist_2:
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
        time.sleep(1)
        # 先获取到页面的html文件
        AirportSelector_exist_br = urllib.request.urlopen(ele['url'])
        # 因为直接解析的列表中存在不可解析的br，所以这里要先替换掉页面中的br标签，再解析
        AirportSelector_nonExist_br = etree.HTML(
            str(AirportSelector_exist_br.read().decode().replace('<br />', ',')))
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
