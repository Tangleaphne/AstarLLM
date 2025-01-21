import requests

def check_address_with_api(address, api_key):
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "getaddressinfo",
        "address": address,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}")
    data = response.json()
    return data

# 示例调用
api_key = "9E4WSUMY9FC812Q93VN8S1MGTD15Y3I6P1"
address = "0x0000000000000000000000000000000000000000"
result = check_address_with_api(address, api_key)
print(result)
