
import os
import json
import requests

# 确保 Base 目录存在
os.makedirs("Base4", exist_ok=True)

# 读取 DApp 列表
with open("dataprocess/DAppdata.js", "r", encoding="utf-8") as f:
    content = f.read()
start = content.find("data = [")
end = content.rfind("]") + 1
data_json = content[start + len("data = "):end]
dapps = json.loads(data_json)

# GPT API 配置
GPT_API_URL = "https://api.openai.com/v1/chat/completions"
GPT_API_KEY = os.getenv("GPT_API_KEY")  

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GPT_API_KEY}"
}

# 循环分析每个 DApp
for item in dapps:
    name = item["DApp 名称"]
    doc_url = item["功能文档链接"]
    code_url = item["源码链接"]

    # 提取英文名用于保存文件
    english_name = "".join([c for c in name if c.isalnum() or c in ("-", "_")])

    output_path = f"Base3/{english_name}_Base_Analysis.md"
    if os.path.exists(output_path):
        print(f"已存在：{output_path}，跳过分析。")
        continue

    prompt = f"""
我需要你帮我审计智能合约，判断某个DApp是否有欺诈或误导用户。请根据其文档（{doc_url}）和源码（{code_url}）进行对比分析：
通过对比文档描述和审计代码，以下是一些关键点的分析：（此处请补充你对比源码与文档后得出的判断，重点是详细分析审计代码各个功能合约是否存在对用户造成损失威胁的漏洞与逻辑问题、然后对比前端网页描述文档说明与代码逻辑不一致的内容或隐藏信息等）。
请按以下格式回复，包含你分析出的源码哪些功能或函数存在对用户造成损失威胁的漏洞与逻辑问题、文档和代码一致性的评估、是否存在误导构成骗局等结论。字数不做限制，越详细越好。
"""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "你是一个智能合约审计专家，擅长分析智能合约与DApp文档之间是否一致，有无欺诈成分。"},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        print(f"正在分析：{name}...")
        response = requests.post(GPT_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(reply)

        print(f"分析完成：{output_path}")
    except Exception as e:
        print(f"分析失败：{name}，错误：{e}")
