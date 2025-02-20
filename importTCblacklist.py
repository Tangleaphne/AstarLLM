from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import os
import time
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

# 目标网站（Tornado-cash 地址）
ETHERSCAN_BLOCKED_URL = "https://etherscan.io/accounts/label/tornado-cash?subcatid=undefined&size=25&start={}&col=1&order=asc"

# 设置 Selenium 浏览器选项
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 无头模式
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")

# 启动 WebDriver
driver = webdriver.Chrome(options=options)
driver.get("https://etherscan.io")  # 先访问主站，以便后续添加 Cookie

# 添加 Cookies（绕过 Cloudflare）
cookies = [
    {"name": "etherscan_offset_datetime", "value": "+8"},
    {"name": "__stripe_mid", "value": "a2a72898-46d4-4096-a730-185094ba344d11a3be"},
    {"name": "etherscan_userid", "value": "syrena"},
    {"name": "etherscan_autologin", "value": "True"},
    {"name": "etherscan_pwd", "value": "4792:Qdxb:fwkKwZJcFAzr1bfqK8rouzfX1Ax20p0PIA/WRe8LZhU="},
    {"name": "etherscan_switch_token_amount_value", "value": "value"},
    {"name": "etherscan_cookieconsent", "value": "True"},
    {"name": "ASP.NET_SessionId", "value": "fslg3a122cgof3ohafhjrcop"},
    {"name": "__cflb", "value": "02DiuFnsSsHWYH8WqVXaqGvd6BSBaXQLU4mmxhHw7uwF2"},
    {"name": "_gid", "value": "GA1.2.2079701353.1740049106"},
    {"name": "cf_clearance", "value": "GmNUQGqeWyojS4yYATtipdTMledBiMT6gcaquLXrWfw-1740059213-1.2.1.1-m0lcb0yg7zbtQVTcuMcBSwLb4yxOQFtncHjRsZoae0Fvw8yNVeF8a.LfOIbZVmbfpDNKPt8cRlXj8aARv3tz.02Jfr5Iaqp0vu.3f2Iql3MKG_.JVVsoI2ik3HOYTMlhiUkm6fUa5qrgt0HVahQ76XHkJPzDBZQ_ZB5Yyd_Dw1tyvr_rQsP0l7406EndST_G0S9GHdgE32QG9RaAyGH1NbFm78MLuYePAP9gQ9UjihyQDJcEKtPsw7GIhJe.ozvk6gzU6B.FCfa4Zk_EltKDnssLAyH9L3uKz0zV7Z0rWZwPn1eP1LqBNCAYz721tRX7Ghn4SO02GDB5ZfmfupM_FQ"},
    {"name": "_ga_T1JC9RNQXV", "value": "GS1.1.1740059211.17.1.1740059344.60.0.0"},
    {"name": "_ga", "value": "GA1.2.4619059.1733811211"},
    {"name": "_gat_gtag_UA_46998878_6", "value": "1"},
]

# 添加 Cookie
for cookie in cookies:
    driver.add_cookie(cookie)

# 连接 MySQL
def connect_db():
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        return conn
    except pymysql.Error as e:
        print(f"数据库连接失败: {e}")
        return None

# 创建数据库表
def create_blocked_table():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tornadocash_blacklist (
                id INT AUTO_INCREMENT PRIMARY KEY,
                address VARCHAR(255) UNIQUE
            )
        """)
        conn.commit()
        conn.close()
        print("黑名单表已创建")

# 爬取封禁地址并存入 MySQL
def fetch_and_store_tornadocash_blacklist(max_addresses=60):
    addresses = set()
    start = 0

    while len(addresses) < max_addresses:
        url = ETHERSCAN_BLOCKED_URL.format(start)
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )

        # 提取地址
        copy_buttons = driver.find_elements(By.CSS_SELECTOR, "a.js-clipboard.link-secondary[data-clipboard-text]")
        if not copy_buttons:
            print(f"已爬取所有地址，停止爬取（start={start}）。")
            break

        for button in copy_buttons:
            full_address = button.get_attribute("data-clipboard-text")
            addresses.add(full_address)

        print(f"已爬取 {len(copy_buttons)} 个新地址，总计 {len(addresses)} 个。")
        start += 25

    # 存入数据库
    save_to_db(addresses)

# 存入 MySQL
def save_to_db(addresses):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        for address in addresses:
            try:
                cursor.execute("INSERT IGNORE INTO tornadocash_blacklist (address) VALUES (%s)", (address,))
            except pymysql.Error as e:
                print(f"数据库插入失败: {e}")

        conn.commit()
        conn.close()
        print("TC名单已存入数据库")

# 运行
if __name__ == "__main__":
    create_blocked_table()
    fetch_and_store_tornadocash_blacklist()
    driver.quit()
