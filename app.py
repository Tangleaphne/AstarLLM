from flask import Flask, render_template, request, jsonify
from config import load_config
from ethereum import fetch_contract_code, save_contract_analysis
import logging
import requests
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


app = Flask(__name__)
load_config()  # 加载配置

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_contract_code", methods=["POST"])
def get_contract_code():
    data = request.json
    recipient = data.get("recipient", "").strip()

    if not recipient:
        return jsonify({"error": "Recipient address is required."}), 400

    try:
        # 获取合约代码并分析
        source_code, address_dir = fetch_contract_code(recipient)
        analysis_path = save_contract_analysis(address_dir, recipient)

        # 返回成功提示信息和分析文件路径
        return jsonify({
            "message": "Contract source code fetched and saved successfully.",
            "analysis_path": analysis_path,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.json
    recipient = data.get("recipient")
    token = data.get("token")
    amount = data.get("amount")
    intention = data.get("intention")

    if not all([recipient, token, amount, intention]):
        return jsonify({"reply": "Please provide all required fields: Recipient, Token, Amount, Intention."})

    # 定义文件路径
    share_dir = os.getenv("SHARE_DIR")
    source_code_path = os.path.join(share_dir, recipient, "SourceCode.sol")
    analysis_path = os.path.join(share_dir, recipient, "analysis.md")

    # 检查文件是否存在
    if not os.path.exists(source_code_path):
        return jsonify({"reply": f"Source code for recipient {recipient} not found. Please fetch it first."})
    if not os.path.exists(analysis_path):
        return jsonify({"reply": f"Slither analysis for recipient {recipient} not found. Please analyze it first."})

    # 构造简化后的 GPT 提示
    gpt_prompt = (
        f"You are an assistant providing investment advice to non-technical users. "
        f"The recipient address is {recipient}, and the user intends to invest {amount} {token}. "
        f"Based on the contract analysis report:\n\n"
        f"{open(analysis_path, 'r', encoding='utf-8').read()}\n\n"
        "Please provide a clear and concise investment suggestion. Avoid technical jargon and focus on whether "
        "the user should proceed with the investment, highlighting key risks or reasons."
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('GPT_API_KEY')}",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": gpt_prompt}
        ]
    }

    try:
        response = requests.post(os.getenv("GPT_API_URL"), headers=headers, json=payload)
        response_data = response.json()
        gpt_reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response from the model.")
        return jsonify({"reply": gpt_reply})
    except Exception as e:
        logger.error(f"Error calling GPT API: {str(e)}")
        return jsonify({"reply": f"Error calling GPT API: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
