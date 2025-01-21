import pymysql
from queue import Queue
from flask import Flask, render_template, request, jsonify
from web3 import Web3
from dotenv import load_dotenv
import os
import requests
import logging
import atexit

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 加载 .env 文件
load_dotenv(dotenv_path=".env")
INFURA_URL = os.getenv("INFURA_URL")
GPT_API_KEY = os.getenv("GPT_API_KEY")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "test2")

if not INFURA_URL:
    raise ValueError("Error: INFURA_URL is not set in the .env file.")
if not GPT_API_KEY:
    raise ValueError("Error: GPT_API_KEY is not set in the .env file.")
if not ETHERSCAN_API_KEY:
    raise ValueError("Error: ETHERSCAN_API_KEY is not set in the .env file.")

# 初始化 Flask 应用
app = Flask(__name__)

# 配置以太坊节点连接
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Ethereum network.")

# 配置 GPT API
GPT_API_URL = "https://api.openai.com/v1/chat/completions"

class Pool:
    def __init__(self, host, user, password, database, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        for _ in range(pool_size):
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.pool.put(connection)

    def get_connection(self):
        return self.pool.get()

    def return_connection(self, connection):
        self.pool.put(connection)

    def close_all_connections(self):
        while not self.pool.empty():
            connection = self.pool.get()
            connection.close()

# 初始化数据库连接池
pool = Pool(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    pool_size=5
)

# 确保数据库表存在
def ensure_table_exists():
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blocked_addresses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                address VARCHAR(255) UNIQUE
            )
        """)
        connection.commit()
    except Exception as e:
        logging.error(f"Error ensuring table exists: {e}")
    finally:
        pool.return_connection(connection)

ensure_table_exists()

@app.route("/")
def index():
    return render_template("index.html")

# 检测地址是否在本地黑名单数据库中
def is_address_blacklisted(address):
    """
    查询数据库，判断地址是否在黑名单中
    """
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM blocked_addresses WHERE address = %s"
        cursor.execute(query, (address.lower(),))  # 转为小写以匹配
        result = cursor.fetchone()
        return result[0] > 0  # 如果返回的计数大于 0，则地址在黑名单中
    except Exception as e:
        logging.error(f"Database query error: {e}")
        return False
    finally:
        pool.return_connection(connection)

@app.route("/check_blacklist", methods=["POST"])
def check_blacklist():
    """
    检测地址是否在本地黑名单数据库中
    """
    try:
        data = request.json
        recipient = data.get("recipient", "").strip()

        if not recipient:
            return jsonify({"error": "Recipient address is required."}), 400

        if not Web3.is_address(recipient):
            return jsonify({"error": "Invalid Ethereum address."}), 400

        # 查询数据库，判断地址是否在黑名单中
        if is_address_blacklisted(recipient):
            return jsonify({"status": "unsafe", "message": "Address is blacklisted."})
        else:
            return jsonify({"status": "safe", "message": "Address is not blacklisted."})

    except Exception as e:
        logging.error(f"Error in /check_blacklist: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# 在应用关闭时，释放数据库连接池
@atexit.register
def close_pool():
    pool.close_all_connections()

@app.route("/get_contract_abi", methods=["POST"])
def get_contract_abi():
    """
    使用 Etherscan API 提取合约 ABI
    """
    try:
        # 获取请求数据
        data = request.json
        recipient = data.get("recipient", "").strip()

        # 验证输入
        if not recipient:
            return jsonify({"error": "Recipient address is required."}), 400

        if not Web3.is_address(recipient):
            return jsonify({"error": "Invalid Ethereum address."}), 400

        # 调用 Etherscan API 获取 ABI
        etherscan_url = "https://api.etherscan.io/api"
        params = {
            "module": "contract",
            "action": "getabi",
            "address": recipient,
            "apikey": ETHERSCAN_API_KEY,
        }
        response = requests.get(etherscan_url, params=params)
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch ABI: {response.status_code} {response.reason}"}), 500

        result = response.json()
        if result["status"] != "1":
            return jsonify({"error": f"Etherscan error: {result['result']}"}), 400

        abi = result["result"]  # 获取 ABI

        # 返回 ABI
        return jsonify({"abi": abi})

    except Exception as e:
        logging.error(f"Error in /get_contract_abi: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route("/get_contract_bytecode", methods=["POST"])
def get_contract_bytecode():
    """
    获取以太坊智能合约的字节码
    """
    try:
        # 获取请求数据
        data = request.json
        recipient = data.get("recipient", "").strip()

        # 验证输入
        if not recipient:
            return jsonify({"error": "Recipient address is required."}), 400

        if not Web3.is_address(recipient):
            return jsonify({"error": "Invalid Ethereum address."}), 400

        # 获取字节码
        bytecode = web3.eth.get_code(recipient).hex()
        if not bytecode or bytecode == "0x":
            return jsonify({"error": "No contract found at the specified address."}), 404

        return jsonify({"bytecode": bytecode})
    except Exception as e:
        logging.error(f"Error in /get_contract_bytecode: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route("/analyze_transaction", methods=["POST"])
def analyze_transaction():
    """
    调用 ChatGPT API 分析智能合约的交易意图和风险
    """
    try:
        # 获取请求数据
        data = request.json
        if not data:
            return jsonify({"error": "Invalid request. No data provided."}), 400

        recipient = data.get("recipient", "").strip()
        token = data.get("token", "").strip()
        amount = data.get("amount", "").strip()
        intention = data.get("intention", "").strip()

        # 验证输入
        if not recipient or not token or not amount or not intention:
            return jsonify({"error": "Please provide all fields: recipient, token, amount, and intention."}), 400

        if not Web3.is_address(recipient):
            return jsonify({"error": "Invalid Ethereum address."}), 400

        try:
            amount = float(amount)
            if amount <= 0:
                return jsonify({"error": "Amount must be a positive number."}), 400
        except ValueError:
            return jsonify({"error": "Amount must be a valid number."}), 400

        # 获取字节码
        bytecode = web3.eth.get_code(recipient).hex()
        if bytecode == "0x":
            return jsonify({"error": "No contract found at the specified address."}), 404

        # 获取abi
        etherscan_url = "https://api.etherscan.io/api"
        params = {
            "module": "contract",
            "action": "getabi",
            "address": recipient,
            "apikey": ETHERSCAN_API_KEY,
        }
        abi_response = requests.get(etherscan_url, params=params)
        if abi_response.status_code != 200:
            return jsonify({"error": f"Failed to fetch ABI: {abi_response.status_code} {abi_response.reason}"}), 500

        abi_result = abi_response.json()
        if abi_result["status"] != "1":
            return jsonify({"error": f"Etherscan error: {abi_result['result']}"}), 400

        abi = abi_result["result"]  # 获取 ABI 数据

        # 构造 GPT 请求的输入内容
        gpt_prompt = (
            f"Transaction details:\n"
            f"- Recipient address: {recipient}\n"
            f"- Token: {token}\n"
            f"- Amount: {amount}\n"
            f"- Intention: {intention}\n\n"
            f"The bytecode of the contract at the recipient address is:\n\n{bytecode}\n\n"
            f"Here is the ABI (Application Binary Interface) of the contract:\n\n{abi}\n\n"
            f"Please analyze this transaction and assess the potential risks, including vulnerabilities in the contract, "
            f"and provide suggestions based on the user's intention."
        )

        # 调用 GPT API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GPT_API_KEY}",
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an expert in Ethereum smart contract bytecode and transaction analysis. And response in Chinese."},
                {"role": "user", "content": gpt_prompt}
            ]
        }

        response = requests.post(GPT_API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            try:
                error_details = response.json()
                error_message = error_details.get("error", {}).get("message", "Unknown error from GPT API.")
            except Exception:
                error_message = "Unable to parse error message from GPT API."
            return jsonify({"error": f"GPT API error: {response.status_code} {response.reason}. Details: {error_message}"}), 500

        # 提取 GPT API 的返回数据
        response_data = response.json()
        gpt_reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response from the model.")

        # 返回结果
        return jsonify({
            "recipient": recipient,
            "token": token,
            "amount": amount,
            "intention": intention,
            "bytecode": bytecode,
            "abi": abi,
            "analysis": gpt_reply
        })

    except requests.exceptions.RequestException as e:
        logging.error(f"GPT API communication error: {e}")
        return jsonify({"error": f"Failed to communicate with GPT API: {str(e)}"}), 502

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# 启动应用
if __name__ == "__main__":
    app.run(debug=True)
