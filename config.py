import os
from dotenv import load_dotenv
from typing import Optional


# === .env ロード ===
load_dotenv()

def _env(name: str, default: Optional[str] = None, required: bool = False) -> str:
    val = os.getenv(name, default)
    if required and not val:
        raise RuntimeError(f"Environment variable '{name}' is required but not set")
    return val

class Settings:
    """
    共通 + サフィックス付き設定を読み込んで、settings.env によって環境切替を可能にする
    """

    def __init__(self, env_suffix: str = ""):
        self.suffix = env_suffix.lower().strip()  # "paper", "book", "academic" など

        # 共通設定
        self.NOTION_API_KEY = _env("NOTION_API_KEY", required=True)
        self.NOTION_VERSION = _env("NOTION_VERSION", "2022-06-28")
        self.DISCORD_WEBHOOK_URL = _env("DISCORD_WEBHOOK_URL", required=True)
        self.MESSAGE_TEMPLATE = _env("MESSAGE_TEMPLATE", "{greeting}\n{title}\n{url}")

        # 環境ごとのサフィックス付き設定
        self.NOTION_DATABASE_ID = _env(f"NOTION_DATABASE_{self.suffix}", required=True)
        self.MESSAGE_GREETING = _env(f"MESSAGE_GREETING_{self.suffix}", "おはようございます．今日の論文は.....")

        prop_list_raw = _env(f"SELECTED_PROPERTIES_{self.suffix}", "Name,Done,URL")
        self.SELECTED_PROPERTIES = [p.strip() for p in prop_list_raw.split(",") if p.strip()]

    def __repr__(self):
        return (
            f"Settings(env_suffix='{self.suffix}')\n"
            f"NOTION_API_KEY=****{self.NOTION_API_KEY[-4:]}\n"
            f"NOTION_DATABASE_ID={self.NOTION_DATABASE_ID}\n"
            f"NOTION_VERSION={self.NOTION_VERSION}\n"
            f"DISCORD_WEBHOOK_URL={self.DISCORD_WEBHOOK_URL[:40]}...\n"
            f"MESSAGE_GREETING={self.MESSAGE_GREETING}\n"
            f"MESSAGE_TEMPLATE={self.MESSAGE_TEMPLATE}\n"
            f"SELECTED_PROPERTIES={self.SELECTED_PROPERTIES}"
        )

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python config.py <env_suffix>")
        print("Example: python config.py paper")
        sys.exit(1)

    suffix = sys.argv[1]
    settings = Settings(env_suffix=suffix)

    print("\n=== .env 読み込み確認 ===")
    print(settings)
    print("==========================\n")
