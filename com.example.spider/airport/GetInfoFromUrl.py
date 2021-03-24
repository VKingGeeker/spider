# 定义字符串处理方法
import os
import urllib.request

import xlwt
from lxml import etree

'''
读取country_url.txt，访问每个国家的所有url，获取到机场的信息，保存到机场信息.xls中
'''

def str_format(str):
    if str.find(',') == 0:
        return str.replace('\t', '').replace('\n', '').replace('\r', '')[1:]
    else:
        return str.replace('\t', '').replace('\n', '').replace('\r', '')


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

# 从url文件中获取url并遍历解析
file_read_obj = open("d:/python/country_url.txt", 'r')
lines = file_read_obj.readlines()

for line in lines:
    # print(line.replace('\n', ''))
    list = line.replace('\n', '').split(',')
    ele = {'continent': list[0], 'country': list[1], 'url': list[2]}

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
        # time.sleep(1)
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
