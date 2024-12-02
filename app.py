from flask import Flask, render_template, request, jsonify
from web3 import Web3

app = Flask(__name__)

# 配置以太坊节点连接（这里使用 Infura 示例）
INFURA_URL = "https://mainnet.infura.io/v3/a2f188a2d48c4422a2d84c08231d5db9"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

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

    # 模拟 AI 的反馈逻辑
    if not recipient or not token or not amount or not intention:
        reply = "Please provide all the required fields: Recipient, Token, Amount, and Intention."
    else:
        reply = (
            f"The recipient ({recipient}) appears risky. The token ({token}) "
            f"might be involved in volatile transactions. Your intention ({intention}) "
            f"could be better clarified to avoid risks. The amount ({amount}) is significant, "
            "please proceed with caution."
        )

    return jsonify({"reply": reply})

@app.route("/get_contract_code", methods=["POST"])
def get_contract_code():
    data = request.json
    recipient = data.get("recipient", "").strip()

    # 验证输入是否为空
    if not recipient:
        return jsonify({"error": "Recipient address is required."}), 400

    # 验证是否为合法的以太坊地址
    if not Web3.is_address(recipient):
        return jsonify({"error": "Invalid Ethereum address."}), 400

    try:
        # 获取合约字节码
        bytecode = web3.eth.get_code(recipient).hex()
        if bytecode == "0x":  # 检查字节码是否为空
            return jsonify({"error": "No contract found at the specified address."}), 404

        return jsonify({"code": bytecode})  # 成功返回合约字节码
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
