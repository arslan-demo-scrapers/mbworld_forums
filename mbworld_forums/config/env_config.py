import os
from dotenv import load_dotenv

load_dotenv()


class EnvConfig:
    PROXY_USERNAME = os.getenv("PROXY_USERNAME")
    PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")

