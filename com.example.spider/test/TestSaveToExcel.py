
import os

# 表头
import xlwt

table_head = ['洲', '国家', '城市_中文名', '城市_英文名', '机场_中文名', '机场_英文名', '机场三字码', '机场四字码']
# 工作簿
book = xlwt.Workbook()
# 工作表
sheet = book.add_sheet('airport')
# 行数
row = 0

for item in range(len(table_head)):
    sheet.write(row, item, table_head[item])

column_data = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                   'H']
row+=1
for item in range(len(column_data)):
    sheet.write(row, item, column_data[item])



db_folder = 'd:/python'
if not os.path.exists('d:/python'):
    os.makedirs('d:/python')

xls_path = os.path.join(db_folder, "test.xls")
book.save(xls_path)