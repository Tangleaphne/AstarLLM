from flask import Flask, render_template, request, jsonify
from web3 import Web3
import requests
from dotenv import load_dotenv
import os
import re
import time
import traceback  # 添加错误日志模块

# 加载 .env 文件
load_dotenv(dotenv_path=".env")

app = Flask(__name__)

# 配置 Etherscan API
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_URL = os.getenv("ETHERSCAN_URL")

print("Loaded Etherscan API Key:", ETHERSCAN_API_KEY)
print("Loaded Etherscan URL:", ETHERSCAN_URL)

# Tornado Cash 地址列表（ETH 混币池）
TORNADO_CASH_ADDRESSES = {
    "0x1111111254EEB25477B68fb85Ed929f73A960582",  # 1 ETH 池
    "0x2222221254EEB25477B68fb85Ed929f73A960582",  # 10 ETH 池
    "0x3333331254EEB25477B68fb85Ed929f73A960582",  # 100 ETH 池
}

# 已知诈骗 / 黑名单地址（可扩展）
BLACKLIST_ADDRESSES = {
    "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "0x0000000000000000000000000000000000000E33",
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze_risk", methods=["POST"])
def analyze_risk():
    try:
        print("✅ Received request at /analyze_risk")  # 记录 API 请求
        data = request.json
        print(f"🔍 Received data: {data}")  # 记录请求数据

        recipient = data.get("recipient", "").strip().lower()

        if not recipient:
            return jsonify({"error": "Recipient address is required."}), 400

        if not Web3.is_address(recipient):
            return jsonify({"error": "Invalid Ethereum address."}), 400

        # 获取交易历史
        transactions = get_transactions(recipient)
        token_transactions = get_token_transactions(recipient)

        all_transactions = transactions + token_transactions
        if not all_transactions:
            return jsonify({"error": "No transactions found."}), 404

        risk_report = {
            "blacklist_interaction": False,
            "high_frequency_activity": False,
            "tornado_cash_involvement": False,
            "high_risk_addresses": set(),
            "transaction_volume": len(all_transactions),
            "timestamps": [],
        }

        for tx in all_transactions[:100]:  # 仅分析最近 100 笔交易
            from_addr = tx.get("from", "").lower()
            to_addr = tx.get("to", "").lower()
            risk_report["timestamps"].append(int(tx.get("timeStamp", "0")))

            # 检查是否与黑名单地址交互
            if from_addr in BLACKLIST_ADDRESSES or to_addr in BLACKLIST_ADDRESSES:
                risk_report["blacklist_interaction"] = True
                risk_report["high_risk_addresses"].add(from_addr)
                risk_report["high_risk_addresses"].add(to_addr)

            # 检查是否与 Tornado Cash 交互
            if from_addr in TORNADO_CASH_ADDRESSES or to_addr in TORNADO_CASH_ADDRESSES:
                risk_report["tornado_cash_involvement"] = True

        # 检测短时间内大量交易
        if len(risk_report["timestamps"]) > 10:
            risk_report["timestamps"].sort()
            time_diffs = [risk_report["timestamps"][i + 1] - risk_report["timestamps"][i] for i in range(len(risk_report["timestamps"]) - 1)]
            avg_time_diff = sum(time_diffs) / len(time_diffs)
            if avg_time_diff < 60:  # 平均时间间隔小于 60 秒
                risk_report["high_frequency_activity"] = True

        # 计算风险评分
        risk_score = 0
        if risk_report["tornado_cash_involvement"]:
            risk_score += 5
        if risk_report["blacklist_interaction"]:
            risk_score += 4
        if risk_report["high_frequency_activity"]:
            risk_score += 2

        # 评估最终风险等级
        if risk_score >= 7:
            risk_level = "🚨 高风险（建议避免交易）"
        elif risk_score >= 3:
            risk_level = "⚠️ 中风险（需进一步审查）"
        else:
            risk_level = "✅ 低风险（未发现异常）"

        return jsonify({
            "recipient": recipient,
            "risk_level": risk_level,
            "risk_report": {
                "blacklist_interaction": risk_report["blacklist_interaction"],
                "high_frequency_activity": risk_report["high_frequency_activity"],
                "tornado_cash_involvement": risk_report["tornado_cash_involvement"],
                "high_risk_addresses": list(risk_report["high_risk_addresses"]),  # 将 set 转换为 list
                "transaction_volume": risk_report["transaction_volume"],
                "timestamps": risk_report["timestamps"]
            }
        })
    
    except Exception as e:
        print("❌ ERROR in analyze_risk:", str(e))
        traceback.print_exc()  # 打印完整错误日志
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


# 获取 ETH 交易历史
def get_transactions(address):
    url = f"{ETHERSCAN_URL}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    print(f"🔍 ETH Transactions API Response: {data}")  # 打印 API 响应
    return data.get("result", []) if data.get("status") == "1" else []


# 获取 ERC-20 交易历史
def get_token_transactions(address):
    url = f"{ETHERSCAN_URL}?module=account&action=tokentx&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    print(f"🔍 ERC-20 Transactions API Response: {data}")  # 打印 API 响应
    return data.get("result", []) if data.get("status") == "1" else []


if __name__ == "__main__":
    app.run(debug=True)
