# import time
# from datetime import datetime
# import requests
# from bs4 import BeautifulSoup
# from web3 import Web3


# def fetch_blocked_addresses(save_to_file=True, file_name="blocked_addresses.txt"):
#     """
#     从 Etherscan 的 blocked 页面抓取黑名单地址，并可选保存到本地文件。
#     """
#     try:
#         url = "https://etherscan.io/accounts/label/blocked"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.9",
#             "Referer": "https://etherscan.io",
#             "Connection": "keep-alive",
#             "Cookie": "etherscan_offset_datetime=+8; __stripe_mid=a2a72898-46d4-4096-a730-185094ba344d11a3be; etherscan_userid=syrena; etherscan_autologin=True; etherscan_pwd=4792:Qdxb:fwkKwZJcFAzr1bfqK8rouzfX1Ax20p0PIA/WRe8LZhU=; ASP.NET_SessionId=wce5i3lt3cg0gkbrcnauyprg; etherscan_switch_token_amount_value=value; __cflb=02DiuFnsSsHWYH8WqVXbZzkeTrZ6gtmGVgpfisTQUZmKr; _gid=GA1.2.1465113033.1737005452; cf_clearance=TdoEtjGKAva7d.W.emYEJaUZUQQ77RZ1f1gmAgzxaRU-1737007727-1.2.1.1-iLSIYL9gcAVveMq9L7Lq.C29yvp2Fbywh2HAn2rA8Rnu56aQ1Msz37IQTfBuyrXNcj6ot7r4qEk2.h6hOo22mE1ATFjnXdedZQ611_v8VByVuxKfuGPvBgpRqsHmk_5oaYqa8JtbnTEPsb0j2iNLuUmnN2bwcn.7Y7oCSHiuv3BEZifuH.pPn5d.3NvrBaYH1VxekHGqgz2_2q3HVYLfOOGinMISpPYWFckDmIipauSA0H3Rcz_ZRamgrHN1whIO15YiXZ3IKwUgNLc_rhZngCYc0TyYrOniCnluWu_5lk07fOdj4Nqy__LrNAi1ACdHMBYFhysuaBHseEHKv8RVDQ; _ga_T1JC9RNQXV=GS1.1.1737007723.5.1.1737008179.60.0.0; _ga=GA1.2.4619059.1733811211; etherscan_cookieconsent=True"
#             }

#         # 发送请求并处理响应
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             raise Exception(f"Failed to fetch page: {response.status_code} {response.reason}")

#         # 使用 BeautifulSoup 解析页面内容
#         soup = BeautifulSoup(response.text, "html.parser")
#         address_elements = soup.select("table tbody tr td:first-child a")  # 提取表格中地址链接

#         # 提取地址列表
#         blocked_addresses = [addr.text.strip() for addr in address_elements if Web3.is_address(addr.text.strip())]

#         # 如果需要保存到本地文件
#         if save_to_file:
#             with open(file_name, "w") as f:
#                 f.write("\n".join(blocked_addresses))
#             print(f"[{datetime.now()}] Blocked addresses saved to {file_name}")

#         return blocked_addresses

#     except Exception as e:
#         print(f"[{datetime.now()}] Error while fetching blocked addresses: {e}")
#         return []


# def run_periodically(interval_hours=24, file_name="blocked_addresses.txt"):
#     """
#     定期运行 fetch_blocked_addresses 保存黑名单数据
#     :param interval_hours: 间隔时间（小时）
#     :param file_name: 保存黑名单地址的文件名
#     """
#     while True:
#         try:
#             print(f"[{datetime.now()}] Updating blacklist...")
#             fetch_blocked_addresses(save_to_file=True, file_name=file_name)
#             print(f"[{datetime.now()}] Blacklist updated successfully.")
#         except Exception as e:
#             print(f"[{datetime.now()}] Error during update: {e}")

#         # 等待下次执行
#         time.sleep(interval_hours * 3600)


# if __name__ == "__main__":
#     # 设置定期更新的时间间隔（以小时为单位）
#     INTERVAL_HOURS = 24

#     # 启动定期任务
#     print(f"[{datetime.now()}] Starting periodic blacklist update. Interval: {INTERVAL_HOURS} hours.")
#     run_periodically(interval_hours=INTERVAL_HOURS)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_and_save_blocked_addresses(file_name="blocked_addresses.txt"):
    url = "https://etherscan.io/accounts/label/blocked"
    
    # 设置浏览器选项
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 无头模式
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")  # 隐藏自动化特征

    # 启动浏览器
    driver = webdriver.Chrome(options=options)
    driver.get("https://etherscan.io") # 打开网站，设置 Cookie

    # 添加你的 Cookie（复制的 Cookie 放在这里）
    cookies = [
        {"name": "etherscan_offset_datetime", "value": "+8"},
        {"name": "__stripe_mid", "value": "a2a72898-46d4-4096-a730-185094ba344d11a3be"},
        {"name": "etherscan_userid", "value": "syrena"},
        {"name": "etherscan_autologin", "value": "True"},
        {"name": "etherscan_pwd", "value": "4792:Qdxb:fwkKwZJcFAzr1bfqK8rouzfX1Ax20p0PIA/WRe8LZhU="},
        {"name": "ASP.NET_SessionId", "value": "wce5i3lt3cg0gkbrcnauyprg"},
        {"name": "etherscan_switch_token_amount_value", "value": "value"},
        {"name": "__cflb", "value": "02DiuFnsSsHWYH8WqVXbZzkeTrZ6gtmGVgpfisTQUZmKr"},
        {"name": "_gid", "value": "GA1.2.1465113033.1737005452"},
        {"name": "cf_clearance", "value": "TdoEtjGKAva7d.W.emYEJaUZUQQ77RZ1f1gmAgzxaRU-1737007727-1.2.1.1-iLSIYL9gcAVveMq9L7Lq.C29yvp2Fbywh2HAn2rA8Rnu56aQ1Msz37IQTfBuyrXNcj6ot7r4qEk2.h6hOo22mE1ATFjnXdedZQ611_v8VByVuxKfuGPvBgpRqsHmk_5oaYqa8JtbnTEPsb0j2iNLuUmnN2bwcn.7Y7oCSHiuv3BEZifuH.pPn5d.3NvrBaYH1VxekHGqgz2_2q3HVYLfOOGinMISpPYWFckDmIipauSA0H3Rcz_ZRamgrHN1whIO15YiXZ3IKwUgNLc_rhZngCYc0TyYrOniCnluWu_5lk07fOdj4Nqy__LrNAi1ACdHMBYFhysuaBHseEHKv8RVDQ"},
        {"name": "etherscan_cookieconsent", "value": "True"},
        {"name": "_ga_T1JC9RNQXV", "value": "GS1.1.1737007723.5.1.1737008312.59.0.0"},
        {"name": "_ga", "value": "GA1.2.4619059.1733811211"},
    ]

    # 将 Cookie 添加到 Selenium
    for cookie in cookies:
        driver.add_cookie(cookie)

    # 刷新页面以应用 Cookie
    driver.get(url)
    # print(driver.page_source)  # 输出完整的 HTML 内容
    try:
        # 显式等待，直到目标表格加载完成
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )
        # print(driver.page_source)  # 输出完整的 HTML 内容
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        addresses = [
            row.find_element(By.CSS_SELECTOR, "td:first-child a").text.strip()
            for row in rows
        ]

        # 保存地址到文件
        with open(file_name, "w") as f:
            f.write("\n".join(addresses))
        print(f"Blocked addresses saved to {file_name}")


    except Exception as e:
        print(f"Error fetching addresses: {e}")
        addresses = []
    finally:
        driver.quit()

    return addresses

# 示例调用
fetch_and_save_blocked_addresses()


# import cloudscraper
# from bs4 import BeautifulSoup

# def fetch_blocked_addresses_with_cloudscraper():
#     url = "https://etherscan.io/accounts/label/blocked"
#     scraper = cloudscraper.create_scraper()

#     response = scraper.get(url)
#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch page: {response.status_code}")

#     soup = BeautifulSoup(response.text, "html.parser")
#     rows = soup.select("table tbody tr")
#     addresses = [row.select_one("td:first-child a").text.strip() for row in rows]

#     return addresses

# # 示例调用
# blocked_addresses = fetch_blocked_addresses_with_cloudscraper()
# print(blocked_addresses)
