from dotenv import load_dotenv
import os
from typing import Optional

'''
.env で設定した変数を読み込んで，settingsに格納する
'''



load_dotenv()

def _env(name: str, default: Optional[str] = None, required: bool = False) -> str:
    val = os.getenv(name, default)
    if required and not val:
        raise RuntimeError(f"Environment variable '{name}' is required but not set")
    return val

class Settings:
    # Notion
    NOTION_API_KEY      = _env("NOTION_API_KEY", required=True)
    NOTION_DATABASE_ID  = _env("NOTION_DATABASE_ID", required=True)
    NOTION_VERSION      = _env("NOTION_VERSION", "2022-06-28")

    # Discord
    DISCORD_WEBHOOK_URL = _env("DISCORD_WEBHOOK_URL", required=True)

    # Messages
    MESSAGE_GREETING    = _env("MESSAGE_GREETING", "おはようございます．今日の論文は.....")
    MESSAGE_TEMPLATE    = _env("MESSAGE_TEMPLATE", "{greeting}\n{title}\n{url}")

    # --- Notionで取得するプロパティ名リスト ---
    SELECTED_PROPERTIES = [s.strip() for s in _env("SELECTED_PROPERTIES", "Name,Done,URL").split(",")]


settings = Settings()



if __name__ == "__main__":
    settings = Settings()

    print("\n\n=== .env テスト出力 ===")
    print("NOTION_API_KEY:", settings.NOTION_API_KEY[:10] + "..." if settings.NOTION_API_KEY else "(未設定)")
    print("NOTION_DATABASE_ID:", settings.NOTION_DATABASE_ID)
    print("NOTION_VERSION:", settings.NOTION_VERSION)
    print("DISCORD_WEBHOOK_URL:", settings.DISCORD_WEBHOOK_URL[:40] + "...")
    print("MESSAGE_GREETING:", settings.MESSAGE_GREETING)
    print("MESSAGE_TEMPLATE:", settings.MESSAGE_TEMPLATE)
    print("SELECTED_PROPERTIES:", settings.SELECTED_PROPERTIES)
    print("========================")
    