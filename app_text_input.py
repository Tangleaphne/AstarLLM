from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# 从环境变量中加载 GPT API Key
GPT_API_URL = "https://api.openai.com/v1/chat/completions"
GPT_API_KEY = os.getenv("GPT_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze_text", methods=["POST"])
def analyze_text():
    data = request.json
    full_text = data.get("text", "")

    if not full_text.strip():
        return jsonify({"reply": "No text received. Please paste something."}), 400

    prompt = (
        "请分析这段代码是否存在常见欺诈行为。"
        f"{full_text}"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_API_KEY}",
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a security auditing assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(GPT_API_URL, headers=headers, json=payload)
        response_data = response.json()
        gpt_reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
        return jsonify({"reply": gpt_reply})
    except Exception as e:
        return jsonify({"reply": f"Error contacting language model: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
