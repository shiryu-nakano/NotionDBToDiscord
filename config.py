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
    def __init__(self):
        # Common
        self.NOTION_API_KEY      = _env("NOTION_API_KEY", required=True)
        self.NOTION_VERSION      = _env("NOTION_VERSION", "2022-06-28")
        self.MESSAGE_TEMPLATE    = _env("MESSAGE_TEMPLATE", "{greeting}\n{title}\n{url}")

        # Respective
        # Paper
        self.NOTION_DATABASE_PAPER = _env("NOTION_DATABASE_PAPER", required=True)
        self.DISCORD_WEBHOOK_URL_PAPER = _env("DISCORD_WEBHOOK_URL_PAPER", required=True)
        self.MESSAGE_GREETING_PAPER    = _env("MESSAGE_GREETING_PAPER", "おはようございます．今日の論文は.....")
        self.SELECTED_PROPERTIES_PAPER = [s.strip() for s in _env("SELECTED_PROPERTIES_PAPER", "Name,Done,URL").split(",")]

        # Book
        self.NOTION_DATABASE_BOOK = _env("NOTION_DATABASE_BOOK", required=True)
        self.DISCORD_WEBHOOK_URL_BOOK = _env("DISCORD_WEBHOOK_URL_BOOK", required=True)
        self.MESSAGE_GREETING_BOOK    = _env("MESSAGE_GREETING_BOOK", "おはようございます．今日の本は.....")
        self.SELECTED_PROPERTIES_BOOK = [s.strip() for s in _env("SELECTED_PROPERTIES_BOOK", "Name,Status,chps").split(",")]

        # Textbook
        self.NOTION_DATABASE_ACADEMIC = _env("NOTION_DATABASE_ACADEMIC", required=True)
        self.DISCORD_WEBHOOK_URL_ACADEMIC = _env("DISCORD_WEBHOOK_URL_ACADEMIC", required=True)
        self.MESSAGE_GREETING_ACADEMIC    = _env("MESSAGE_GREETING_ACADEMIC", "おはようございます．今日の教科書は.....")
        self.SELECTED_PROPERTIES_ACADEMIC = [s.strip() for s in _env("SELECTED_PROPERTIES_ACADEMIC", "Name,Status,Select").split(",")]

        # --- Notionで取得するプロパティ名リスト ---
        self.SELECTED_PROPERTIES = [s.strip() for s in _env("SELECTED_PROPERTIES", "Name,Done,URL").split(",")]

    
    def __repr__(self):
        masked = lambda s: (s[:4] + "..." + s[-4:]) if s and len(s) > 10 else (s or "")
        return (
            f"Settings(suffix='{self.suffix}')\n"
            f"NOTION_DATABASE_ID={self.NOTION_DATABASE_ID}\n"
            f"DISCORD_WEBHOOK_URL(active)={masked(self.DISCORD_WEBHOOK_URL)}\n"
            f"DISCORD_WEBHOOK_URL_PAPER={masked(self.DISCORD_WEBHOOK_URL_PAPER)}\n"
            f"DISCORD_WEBHOOK_URL_BOOK={masked(self.DISCORD_WEBHOOK_URL_BOOK)}\n"
            f"DISCORD_WEBHOOK_URL_ACADEMIC={masked(self.DISCORD_WEBHOOK_URL_ACADEMIC)}"
        )
    def __repr__(self):
        # __init__で定義されている変数を表示するように修正
        masked = lambda s: (s[:8] + "..." + s[-4:]) if s and len(s) > 20 else (s or "")
        return (
            "Settings(\n"
            f"  NOTION_API_KEY: {masked(self.NOTION_API_KEY)}\n"
            f"  NOTION_DATABASE_PAPER: {self.NOTION_DATABASE_PAPER}\n"
            f"  DISCORD_WEBHOOK_URL_PAPER: {masked(self.DISCORD_WEBHOOK_URL_PAPER)}\n"
            f"  NOTION_DATABASE_BOOK: {self.NOTION_DATABASE_BOOK}\n"
            f"  DISCORD_WEBHOOK_URL_BOOK: {masked(self.DISCORD_WEBHOOK_URL_BOOK)}\n"
            f"  NOTION_DATABASE_ACADEMIC: {self.NOTION_DATABASE_ACADEMIC}\n"
            f"  DISCORD_WEBHOOK_URL_ACADEMIC: {masked(self.DISCORD_WEBHOOK_URL_ACADEMIC)}\n"
            )        

settings = Settings()



if __name__ == "__main__":
    try:
        # このブロック内でのみインスタンス化する
        settings = Settings()

        print("\n\n=== .env テスト出力 ===")
        print("--- 共通設定 ---")
        print(f"NOTION_API_KEY: {settings.NOTION_API_KEY[:5]}..." if settings.NOTION_API_KEY else "(未設定)")
        print(f"NOTION_VERSION: {settings.NOTION_VERSION}")
        print(f"MESSAGE_TEMPLATE: {settings.MESSAGE_TEMPLATE}")
        
        print("\n--- 論文 (Paper) ---")
        print(f"NOTION_DATABASE_PAPER: {settings.NOTION_DATABASE_PAPER}")
        print(f"DISCORD_WEBHOOK_URL_PAPER: {settings.DISCORD_WEBHOOK_URL_PAPER[:30]}...")
        print(f"MESSAGE_GREETING_PAPER: {settings.MESSAGE_GREETING_PAPER}")
        print(f"SELECTED_PROPERTIES_PAPER: {settings.SELECTED_PROPERTIES_PAPER}")

        print("\n--- 書籍 (Book) ---")
        print(f"NOTION_DATABASE_BOOK: {settings.NOTION_DATABASE_BOOK}")
        print(f"DISCORD_WEBHOOK_URL_BOOK: {settings.DISCORD_WEBHOOK_URL_BOOK[:30]}...")
        print(f"MESSAGE_GREETING_BOOK: {settings.MESSAGE_GREETING_BOOK}")
        print(f"SELECTED_PROPERTIES_BOOK: {settings.SELECTED_PROPERTIES_BOOK}")

        print("\n--- 教科書 (Academic) ---")
        print(f"NOTION_DATABASE_ACADEMIC: {settings.NOTION_DATABASE_ACADEMIC}")
        print(f"DISCORD_WEBHOOK_URL_ACADEMIC: {settings.DISCORD_WEBHOOK_URL_ACADEMIC[:30]}...")
        print(f"MESSAGE_GREETING_ACADEMIC: {settings.MESSAGE_GREETING_ACADEMIC}")
        print(f"SELECTED_PROPERTIES_ACADEMIC: {settings.SELECTED_PROPERTIES_ACADEMIC}")
        
        print("\n--- __repr__による出力 ---")
        print(settings)

        print("========================")

    except RuntimeError as e:
        print(f"\n[エラー] 設定を読み込めませんでした。")
        print(e)
        print(".envファイルの内容を確認してください。")
