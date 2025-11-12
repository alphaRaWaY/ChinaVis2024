import json

import mysql.connector

# 连接到MySQL数据库
import numpy as np
import os
from dotenv import load_dotenv
# ----------------- 新增連線配置區 -----------------
# 載入 .env 檔案中的所有變數
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    port=DB_PORT,
    password=DB_PASSWORD,
    database=DB_NAME,
)

# 创建游标对象
cursor = conn.cursor()

# 执行查询语句，获取所有城市值和对应的平均月薪
cursor.execute("SELECT city, AVG(`Avg Monthly Salary`) FROM rec_inf GROUP BY city")
city_avg_salary_data = cursor.fetchall()

# 执行查询语句，获取所有城市值和对应的出现次数
cursor.execute("SELECT city, COUNT(*) FROM rec_inf GROUP BY city")
city_count_data = cursor.fetchall()

# 关闭游标
cursor.close()

# 关闭连接
conn.close()

# 提取不同城市值
cities = [record[0] for record in city_avg_salary_data]

# 提取不同城市对应的平均月薪
avg_salaries = np.array([record[1] for record in city_avg_salary_data])

# 构建城市平均月薪的字典，将 Decimal 类型的值转换为浮点数
city_avg_salary_dict = {record[0]: float(record[1]) for record in city_avg_salary_data}

# 构建城市出现次数的字典
city_count_dict = {record[0]: record[1] for record in city_count_data}

# 将 NumPy 数组和字典储存到文件中
np.save('../data/city.npy', cities)
with open('../data/city_avg_salary_dict.json', 'w') as f:
    json.dump(city_avg_salary_dict, f)
with open('../data/city_count_dict.json', 'w') as f:
    json.dump(city_count_dict, f)





