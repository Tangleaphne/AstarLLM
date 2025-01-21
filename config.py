import os
from dotenv import load_dotenv

def load_config():
    load_dotenv(dotenv_path=".env")
    os.environ["SHARE_DIR"] = os.getenv("SHARE_DIR", "./share")
    os.environ["INFURA_URL"] = os.getenv("INFURA_URL", "")
    os.environ["GPT_API_KEY"] = os.getenv("GPT_API_KEY", "")
    os.environ["CONTAINER_ID"] = os.getenv("CONTAINER_ID", "")
