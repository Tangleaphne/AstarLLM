import re

def extract_solidity_version(source_code):
    """
    从 Solidity 源代码中提取版本号。
    """
    match = re.search(r"pragma\s+solidity\s+([~^=<>\d.]+);", source_code)
    if match:
        return re.sub(r"[~^=]", "", match.group(1))
    return "Unknown"
