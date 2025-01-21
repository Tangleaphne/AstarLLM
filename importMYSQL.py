import pymysql

def import_txt_to_mysql(txt_file, db_host, db_user, db_password, db_name):
    """
    将 .txt 文件数据导入到 MySQL 数据库
    """
    # 连接 MySQL 数据库
    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    # 确保目标表存在
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocked_addresses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            address VARCHAR(255) UNIQUE
        )
    """)

    # 读取 .txt 文件并插入数据库
    with open(txt_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            address = line.strip()  # 去掉换行符
            if address:
                try:
                    cursor.execute("INSERT IGNORE INTO blocked_addresses (address) VALUES (%s)", (address,))
                except Exception as e:
                    print(f"Error inserting address {address}: {e}")

    # 提交更改并关闭连接
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data from {txt_file} has been successfully imported into the database.")


# 示例调用
import_txt_to_mysql(
    txt_file="blocked_addresses.txt",  # 替换为你的 .txt 文件路径
    db_host="localhost",               # MySQL 主机
    db_user="root",                    # MySQL 用户名
    db_password="",       # MySQL 密码
    db_name="test2"            # 数据库名称
)
