from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def chat():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    # 模拟一个简单的 AI 回复逻辑
    response = {"reply": f"You said: {user_message}"}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
