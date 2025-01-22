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

@app.route("/analyze_and_advise", methods=["POST"])
def analyze_and_advise():
    data = request.json
    recipient = data.get("recipient", "").strip()
    token = data.get("token","").strip()
    amount = data.get("amount","").strip()
    intention = data.get("intention","").strip()

    if not recipient:
        return jsonify({"error": "Recipient address is required."}), 400

    try:
        # Step 1: 获取合约代码并分析
        source_code, address_dir = fetch_contract_code(recipient)
        analysis_path = save_contract_analysis(address_dir, recipient)

        # Step 2: 读取 Slither 分析内容
        with open(analysis_path, "r", encoding="utf-8") as analysis_file:
            slither_content = analysis_file.read()

        # Step 3: 构造 GPT 请求
        gpt_prompt_security = (
            f"Provide a concise security assessment for a non-technical user based on the following contract analysis. "
            f"The recipient address is {recipient}. The user intends to invest {amount} {token} with the goal of '{intention}'.\n\n"
            f"Analysis:\n{slither_content}\n\n"
            f"Instructions:\n"
            f"1. Start by addressing the user's intention and whether it aligns with the contract's functionality.\n"
            f"2. Highlight any vulnerabilities categorized as 'high' by Slither and explain their potential impact on the investment, "
            f"without delving into technical details.\n"
            f"3. Ignore vulnerabilities ranked as 'medium', 'low', or 'informational'.\n"
            f"4. Conclude with your personal opinion on whether the user should proceed with the investment, clearly stating reasons."
        )

        gpt_prompt_functionality = (
            f"Explain the functionality of this smart contract for a non-technical user. Focus on:\n"
            f"1. Whether the contract can accept {token} for investment.\n"
            f"2. How funds will flow if invested, including where they will go and how they might be used.\n"
            f"3. Any fairness issues, such as uneven fund distribution or biased logic.\n"
            f"4. Whether the contract shows signs of malicious intent, like unusually high fees or exploitable features.\n\n"
            f"Contract Source Code:\n{source_code}"
        )


        gpt_responses = []
        for prompt in [gpt_prompt_security, gpt_prompt_functionality]:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv('GPT_API_KEY')}",
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post(os.getenv("GPT_API_URL"), headers=headers, json=payload)
            gpt_responses.append(response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response."))

        # Step 4: 返回综合结果
        return jsonify({
            "security_assessment": gpt_responses[0],
            "functionality_analysis": gpt_responses[1],
            "analysis_path": analysis_path
        })

    except Exception as e:
        logger.error(f"Error during analysis and advice: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
