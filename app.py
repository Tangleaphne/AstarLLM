from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
