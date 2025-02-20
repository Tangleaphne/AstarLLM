import pymysql
import json
import os
from dotenv import load_dotenv

# 读取 .env 配置
load_dotenv()

# MySQL 配置
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE"),
}

# 连接 MySQL
def connect_db():
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        return conn
    except pymysql.Error as e:
        print(f"数据库连接失败: {e}")

conn = connect_db()
cursor = conn.cursor()

# create Table
cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ofac_addresses (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        address VARCHAR(100) UNIQUE NOT NULL,
                        currency VARCHAR(10) NOT NULL
                    )
                """)

# 读取 OFAC 黑名单
json_file_path = "ofac.json"

with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# 插入数据
for entry in data:
    currency = entry["Currency"]  # 获取币种
    address = entry["Blockchain Address"]  # 获取地址
    cursor.execute("INSERT IGNORE INTO ofac_addresses (address, currency) VALUES (%s, %s)", (address, currency))

# 提交更改并关闭连接
conn.commit()
cursor.close()
conn.close()

print(f"✅ 成功插入 {len(data)} 条受制裁的区块链地址记录！")