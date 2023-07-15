import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
#打开数据库配置文件并读取内容
with open('set\sqlset.txt','r') as file:
    lines = file.readlines()

#初始化连接信息
host=''
dataname=''
username=''
password=''

#提取每一行的信息
for line in lines:
    #查找引号位置
    start_quote = line.find('"')
    end_quote = line.rfind('"')
    #提取引号内信息
    if start_quote != -1 and end_quote != -1:
        value = line[start_quote+1:end_quote]
        #根据变量名存储信息
        if line.startswith('host='):
            host = value
        elif line.startswith('dataname='):
            dataname = value
        elif line.startswith('username='):
            username=value
        elif line.startswith('password='):
            password = value
sql = mysql.connector.connect(host=host,user=username,password=password,database=dataname,charset='utf8mb4')
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{dataname}')
table = input("输入要操作的表")
query = f'SELECT * FROM {table}'
df = pd.read_sql_query(query,engine)
#导出为Excel表格
excel_file = f'{table}_table.xlsx'
df.to_excel(excel_file,index=False)
sql.close()
print(f'数据已经导出到{excel_file}')