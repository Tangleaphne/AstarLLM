from flask import Flask, render_template, request, jsonify
from config import load_config
from ethereum import fetch_contract_code, save_contract_analysis
import logging

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

# @app.route("/get_contract_code", methods=["POST"])
# def get_contract_code():
#     data = request.json
#     recipient = data.get("recipient", "").strip()

#     if not recipient:
#         return jsonify({"error": "Recipient address is required.\n"}), 400

#     try:
#         # 获取合约代码并分析
#         source_code, address_dir = fetch_contract_code(recipient)
#         analysis_path = save_contract_analysis(address_dir, recipient)
#         # logger.debug(f"source: {source_code}")
#         # logger.debug(f"analysis_path: {analysis_path}")
#         return jsonify({"\nsource": source_code, "\nanalysis_path": analysis_path})
#     except Exception as e:
#         return jsonify({"\nerror": str(e)}), 500


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


if __name__ == "__main__":
    app.run(debug=True)
