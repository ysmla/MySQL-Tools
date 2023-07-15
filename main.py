import os
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
def look():
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])

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

sql = mysql.connector.connect(host=host,user = username,password=password,database=dataname,charset='utf8mb4')
cursor = sql.cursor()
print('''
直接输入sql语句执行
输入look查看当前数据库下所有表
输入create创建表
输入exit退出
输入check+表名查看该表下有哪些列
输入dle+表名删除表
输入write将列和值导出为Excel表格
输入add+表名插入值
输入detail查看表下的值
''')
while 1:
    order = input(">>>")
    if order == "look":
        look()
    if order == "exit":
        break
    if order == "create":
        name = input("表名")
        time = int(input("表内含有几个键"))
        keyname = []
        keytype = []
        keylong = []
        keynull = []
        for i in range(time):
            nameinput = input("列名")
            typeinput = input("列类型")
            longinput = input("列长度")
            nullinput = input('列是否可以为空 NOT NULL或空')
            keyname.append(nameinput)
            keytype.append(typeinput)
            keylong.append(longinput)
            keynull.append(nullinput)
        sentence = ''
        for i in range(time):
            sentenceadd = f'{keyname[i]}   {keytype[i]}({int(keylong[i])})  {keynull[i]}'
            if i+1 == time:
                sentenceadd+='\n'
            else:
                sentenceadd+=',\n'
            sentence += sentenceadd
        create_table_query = f"""
        CREATE TABLE {name} (
            id INT PRIMARY KEY AUTO_INCREMENT,
            {sentence}
        )
        """
        cursor.execute(create_table_query)
        sql.commit()
        look()
    if order.startswith('check'):
        parts = order.split(' ')
        table = parts[1]
        query = f'DESCRIBE {table}'
        cursor.execute(query)
        columns = cursor.fetchall()
        for column in columns:
            print(column[0])
    if order.startswith('dle'):
        parts = order.split(' ')
        table = parts[1]
        ask = input("确定删除该表吗？删除后无法恢复，输入删除以继续，输入任意键退出")
        if ask == '删除':
            query = f'DROP TABLE IF EXISTS {table}'
            cursor.execute(query)
            sql.commit()
            look()
        else:
            pass
    if order.startswith('write'):
        os.system('导出.py')
    if order.startswith('add'):
        parts = order.split(' ')
        table = parts[1]
        describe_query = f'DESCRIBE {table}'
        cursor.execute(describe_query)
        #获取表的列信息
        columns = [column[0] for column in cursor.fetchall()]
        values = []
        for column in  columns:
            value = input(f'请输入{column}的值>>>')
            values.append(value)
        #构建插入语句
        insert_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(columns))})"
        #执行插入语句
        cursor.execute(insert_query,values)
        #提交更改
        sql.commit()
        print(f'值已经成功插入到{table}')
    if order=='detail':
        table = input("输入要操作的表")
        columns_query = f'SHOW COLUMNS FROM {table}'
        cursor.execute(columns_query)
        columns = [column[0] for column in cursor.fetchall()]
        #执行查询数据的语句
        data_query = f'SELECT * FROM {table}'
        cursor.execute(data_query)
        #获取所有数据
        data = cursor.fetchall()
        print(columns)
        for row in data:
            print(row)
cursor.close()
sql.close()