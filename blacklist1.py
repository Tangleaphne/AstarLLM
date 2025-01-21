# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# def fetch_and_save_blocked_addresses(file_name="blocked_addresses1.txt"):
#     url = "https://etherscan.io/accounts/label/blocked"

#     # 设置浏览器选项
#     options = webdriver.ChromeOptions()
#     # options.add_argument("--headless")  # 无头模式（调试时可以注释掉）
#     options.add_argument("--disable-gpu")  # 禁用 GPU 加速
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-blink-features=AutomationControlled")  # 隐藏自动化特征

#     # 启动浏览器
#     driver = webdriver.Chrome(options=options)
#     driver.get("https://etherscan.io")  # 打开主站以设置 Cookie

#     # 添加你的 Cookie（根据实际情况填写）
#     cookies = [
#         {"name": "etherscan_offset_datetime", "value": "+8"},
#         {"name": "__stripe_mid", "value": "a2a72898-46d4-4096-a730-185094ba344d11a3be"},
#         {"name": "etherscan_userid", "value": "syrena"},
#         {"name": "etherscan_autologin", "value": "True"},
#         {"name": "etherscan_pwd", "value": "4792:Qdxb:fwkKwZJcFAzr1bfqK8rouzfX1Ax20p0PIA/WRe8LZhU="},
#         {"name": "ASP.NET_SessionId", "value": "wce5i3lt3cg0gkbrcnauyprg"},
#         {"name": "etherscan_switch_token_amount_value", "value": "value"},
#         {"name": "__cflb", "value": "02DiuFnsSsHWYH8WqVXbZzkeTrZ6gtmGVgpfisTQUZmKr"},
#         {"name": "_gid", "value": "GA1.2.1465113033.1737005452"},
#         {"name": "cf_clearance", "value": "TdoEtjGKAva7d.W.emYEJaUZUQQ77RZ1f1gmAgzxaRU-1737007727-1.2.1.1-iLSIYL9gcAVveMq9L7Lq.C29yvp2Fbywh2HAn2rA8Rnu56aQ1Msz37IQTfBuyrXNcj6ot7r4qEk2.h6hOo22mE1ATFjnXdedZQ611_v8VByVuxKfuGPvBgpRqsHmk_5oaYqa8JtbnTEPsb0j2iNLuUmnN2bwcn.7Y7oCSHiuv3BEZifuH.pPn5d.3NvrBaYH1VxekHGqgz2_2q3HVYLfOOGinMISpPYWFckDmIipauSA0H3Rcz_ZRamgrHN1whIO15YiXZ3IKwUgNLc_rhZngCYc0TyYrOniCnluWu_5lk07fOdj4Nqy__LrNAi1ACdHMBYFhysuaBHseEHKv8RVDQ"},
#         {"name": "etherscan_cookieconsent", "value": "True"},
#         {"name": "_ga_T1JC9RNQXV", "value": "GS1.1.1737007723.5.1.1737008312.59.0.0"},
#         {"name": "_ga", "value": "GA1.2.4619059.1733811211"},
#     ]

#     # 添加 Cookie
#     for cookie in cookies:
#         driver.add_cookie(cookie)

#     # 刷新页面以应用 Cookie
#     driver.get(url)

#     try:
#         # 等待表格加载完成
#         WebDriverWait(driver, 50).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
#         )

#         # 找到所有复制按钮，更新选择器为精准定位
#         copy_buttons = driver.find_elements(By.CSS_SELECTOR, "a.js-clipboard.link-secondary[data-clipboard-text]")  
#         addresses = []

#         for button in copy_buttons:
#             # 点击复制按钮
#             driver.execute_script("arguments[0].click();", button)
#             time.sleep(0.5)  # 等待复制完成

#             # 获取按钮上的完整地址
#             full_address = button.get_attribute("data-clipboard-text")
#             addresses.append(full_address)

#         # 保存完整地址到文件
#         with open(file_name, "w") as f:
#             f.write("\n".join(addresses))
#         print(f"Blocked addresses saved to {file_name}")

#     except Exception as e:
#         print(f"Error fetching addresses: {e}")
#     finally:
#         driver.quit()

#     return addresses

# # 示例调用
# fetch_and_save_blocked_addresses()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def fetch_and_save_blocked_addresses(file_name="blocked_addresses_full1.txt", max_addresses=114):
    base_url = "https://etherscan.io/accounts/label/blocked?subcatid=undefined&size=25&start={}&col=1&order=asc"

    # 设置浏览器选项
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 无头模式（调试时可注释掉）
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")  # 隐藏自动化特征

    # 启动浏览器
    driver = webdriver.Chrome(options=options)
    driver.get("https://etherscan.io")  # 打开主站以设置 Cookie

    # 添加你的 Cookie（根据实际情况填写）
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

    # 添加 Cookie
    for cookie in cookies:
        driver.add_cookie(cookie)

    # 初始化存储地址列表
    addresses = []

    try:
        # 遍历所有页面
        start = 675
        while len(addresses) < max_addresses:
            # 构造当前页 URL
            url = base_url.format(start)
            driver.get(url)

            # 等待表格加载完成
            WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
            )

            # 找到当前页所有复制按钮
            copy_buttons = driver.find_elements(By.CSS_SELECTOR, "a.js-clipboard.link-secondary[data-clipboard-text]")

            # 如果当前页没有地址，说明到达最后一页
            if not copy_buttons:
                print(f"No more addresses found. Stopping at start={start}.")
                break

            # 提取地址
            for button in copy_buttons:
                full_address = button.get_attribute("data-clipboard-text")
                addresses.append(full_address)

                # 如果达到最大数量，停止爬取
                if len(addresses) >= max_addresses:
                    print("Reached the limit of addresses. Stopping...")
                    break

            # 打印当前页信息
            print(f"Page starting at {start}: {len(copy_buttons)} addresses found.")

            # 更新 `start` 参数，跳转下一页
            start += 25

        # 保存完整地址到文件
        with open(file_name, "w") as f:
            f.write("\n".join(addresses))
        print(f"Blocked addresses saved to {file_name}")

    except Exception as e:
        print(f"Error fetching addresses: {e}")
    finally:
        driver.quit()

    return addresses


# 示例调用
fetch_and_save_blocked_addresses()
