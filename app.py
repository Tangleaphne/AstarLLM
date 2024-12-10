from flask import Flask, render_template, request, jsonify
from web3 import Web3
import requests
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv(dotenv_path=".env")

app = Flask(__name__)

# 配置以太坊节点连接（这里使用 Infura 示例）
INFURA_URL = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# GPT-4o-mini API 配置
GPT_API_URL = "https://api.openai.com/v1/chat/completions"
GPT_API_KEY = os.getenv("GPT_API_KEY")
# print("Loaded API Key:", GPT_API_KEY)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.json
    recipient = data.get("recipient")
    token = data.get("token")
    amount = data.get("amount")
    intention = data.get("intention")

    # 检查输入是否完整
    if not recipient or not token or not amount or not intention:
        return jsonify({"reply": "Please provide all the required fields: Recipient, Token, Amount, and Intention."})

    # 模拟获取智能合约字节码
    try:
        code = web3.eth.get_code(recipient).hex()
        if code == "0x":
            return jsonify({"reply": "No contract found at the specified address."})
    except Exception as e:
        return jsonify({"reply": f"Error fetching contract code: {str(e)}"})

    # 构造 GPT 请求的输入内容
    gpt_prompt = (
        f"The recipient address is {recipient}. The token involved is {token}, "
        f"the amount is {amount}, and the user intention is '{intention}'. The contract source code is:\n\n{code}\n\n"
        "Please analyze the contract for risks and provide suggestions."
    )

    # 调用 GPT API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_API_KEY}",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": gpt_prompt}
        ]
    }

    try:
        response = requests.post(GPT_API_URL, headers=headers, json=payload)
        response_data = response.json()
        # print("Full GPT Response:", response_data)  # 调试用
        gpt_reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response from the model.")
    except Exception as e:
        gpt_reply = f"Error calling GPT API: {str(e)}"

    # 返回 GPT 的回复
    return jsonify({"reply": gpt_reply})

@app.route("/get_contract_code", methods=["POST"])
def get_contract_code():
    data = request.json
    recipient = data.get("recipient", "").strip()

    if not recipient:
        return jsonify({"error": "Recipient address is required."}), 400

    if not Web3.is_address(recipient):
        return jsonify({"error": "Invalid Ethereum address."}), 400

    try:
        # 调用 Etherscan API 获取源码
        ETHERSCAN_API_URL = "https://api.etherscan.io/api"
        ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")  # 从环境变量中获取 API 密钥
        print("Loaded API Key:", ETHERSCAN_API_KEY)

        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": recipient,
            "apikey": ETHERSCAN_API_KEY,
        }

        # 调用 Etherscan API
        response = requests.get(ETHERSCAN_API_URL, params=params)
        response_data = response.json()

        # 检查 API 返回的状态
        if response_data["status"] != "1":
            return jsonify({"error": response_data.get("result", "Error fetching contract source.")}), 400

        # 获取合约源码
        source_code = response_data["result"][0].get("SourceCode", "No source code found.")
        if not source_code:
            return jsonify({"error": "No source code found at the specified address."}), 404

        return jsonify({"source": source_code})  # 返回源码
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
