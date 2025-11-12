import mysql.connector

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
def get_salary_ranges():
    # 连接数据库
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        port=DB_PORT,
        password=DB_PASSWORD,
        database=DB_NAME,
    )

    # 定义SQL查询
    sql_query = """
        SELECT `Avg Monthly Salary`
        FROM rec_inf
        ORDER BY `Avg Monthly Salary`
    """

    # 执行查询
    cursor = conn.cursor()
    cursor.execute(sql_query)

    # 获取结果
    salaries = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    # 将结果转换为列表
    salaries = [salary[0] for salary in salaries]

    # 计算每个段的大小
    segment_size = len(salaries) // 3
    salary_ranges = []

    for i in range(3):
        start_index = i * segment_size
        end_index = start_index + segment_size
        if i == 2:  # 最后一段
            end_index = len(salaries)
        segment_salaries = salaries[start_index:end_index]
        salary_range = (min(segment_salaries), max(segment_salaries))
        salary_ranges.append(salary_range)

    return salary_ranges


# 获取工资范围
ranges = get_salary_ranges()

# 输出每个段的最大值和最小值
for i, salary_range in enumerate(ranges, start=1):
    print(f"Segment {i}: Min Salary = {salary_range[0]}, Max Salary = {salary_range[1]}")
