# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # .env をカレントディレクトリから読み込む

def env(name: str, default: str | None = None, required: bool = False) -> str:
    val = os.getenv(name, default)
    if required and not val:
        raise RuntimeError(f"Environment variable '{name}' is required but not set")
    return val

class Settings:
    NOTION_API_KEY      = env("NOTION_API_KEY", required=True)
    NOTION_DATABASE_ID  = env("NOTION_DATABASE_ID", required=True)
    NOTION_VERSION      = env("NOTION_VERSION", "2022-06-28")

    DISCORD_WEBHOOK_URL = env("DISCORD_WEBHOOK_URL", required=True)

    MESSAGE_GREETING    = env("MESSAGE_GREETING", "おはようございます．今日の論文は.....")
    MESSAGE_TEMPLATE    = env("MESSAGE_TEMPLATE", "{greeting}\n{title}\n{url}")  # 3行構成

settings = Settings()
