import os
from web3 import Web3
import requests
import subprocess
from analysis import run_slither_analysis

web3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))

def fetch_contract_code(recipient):
    if not Web3.is_address(recipient):
        raise ValueError("Invalid Ethereum address.")

    # 调用 Etherscan API
    ETHERSCAN_API_URL = "https://api.etherscan.io/api"
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": recipient,
        "apikey": os.getenv("ETHERSCAN_API_KEY"),
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    response_data = response.json()

    if response_data['status'] != "1":
        raise ValueError(f"Error fetching contract source code: {response_data.get('result', 'Unknown error')}")


    source_code = response_data["result"][0].get("SourceCode", "")
    if not source_code:
        raise ValueError("No source code found.")

    # 创建地址目录
    address_dir = os.path.join(os.getenv("SHARE_DIR"), recipient)
    os.makedirs(address_dir, exist_ok=True)

    # 保存源码
    source_code_path = os.path.join(address_dir, f"SourceCode.sol")
    with open(source_code_path, "w", encoding="utf-8") as file:
        file.write(source_code)

    return source_code, address_dir


def save_contract_analysis(address_dir, recipient):
    """
    保存合约源码并运行 Slither 分析
    """

    # 调用 Slither 分析
    analysis_path = run_slither_analysis(address_dir, recipient)

    return analysis_path