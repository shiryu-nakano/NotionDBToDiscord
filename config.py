import os
from dotenv import load_dotenv
from typing import Optional, Dict

load_dotenv()

def _env(name: str, default: Optional[str] = None, required: bool = False) -> str:
    val = os.getenv(name, default)
    if required and not val:
        raise RuntimeError(f"Environment variable '{name}' is required but not set")
    return val

class Settings:
    """
    - 共通: NOTION_API_KEY, NOTION_VERSION, MESSAGE_TEMPLATE
    - 環境別: NOTION_DATABASE_<suffix>, MESSAGE_GREETING_<suffix>,
             SELECTED_PROPERTIES_<suffix>, DISCORD_WEBHOOK_URL_<SUFFIX>
    - suffix でアクティブ環境を選択。環境別Webhookは個別変数でも保持。
    """

    def __init__(self, env_suffix: str = "paper"):
        self.suffix = suffix = env_suffix.lower().strip()

        # --- 共通 ---
        self.NOTION_API_KEY   = _env("NOTION_API_KEY", required=True)
        self.NOTION_VERSION   = _env("NOTION_VERSION", "2022-06-28")
        self.MESSAGE_TEMPLATE = _env("MESSAGE_TEMPLATE", "{greeting}\n{title}\n{url}")

        # --- 環境別（DB, メッセージ, プロパティ）---
        self.NOTION_DATABASE_ID  = _env(f"NOTION_DATABASE_{suffix}", required=True)
        self.MESSAGE_GREETING    = _env(f"MESSAGE_GREETING_{suffix}", "おはようございます．今日の論文は.....")
        props_raw                = _env(f"SELECTED_PROPERTIES_{suffix}", "Name,Done,URL")
        self.SELECTED_PROPERTIES = [p.strip() for p in props_raw.split(",") if p.strip()]

        # --- Webhook: 環境ごとに個別保持 + アクティブも用意 ---
        # ※ CI では実行ターゲット以外のWebhookが未設定でも落ちないよう required=False
        self.DISCORD_WEBHOOK_URL_PAPER    = _env("DISCORD_WEBHOOK_URL_PAPER",    required=False)
        self.DISCORD_WEBHOOK_URL_BOOK     = _env("DISCORD_WEBHOOK_URL_BOOK",     required=False)
        self.DISCORD_WEBHOOK_URL_ACADEMIC = _env("DISCORD_WEBHOOK_URL_ACADEMIC", required=False)

        self.DISCORD_WEBHOOK_URLS: Dict[str, Optional[str]] = {
            "paper":    self.DISCORD_WEBHOOK_URL_PAPER,
            "book":     self.DISCORD_WEBHOOK_URL_BOOK,
            "academic": self.DISCORD_WEBHOOK_URL_ACADEMIC,
        }

        # アクティブ（現在実行ターゲット）のWebhook
        #   1) 個別保持に入っていればそれを使う
        #   2) それでも空なら、環境名から直接読み直して必須化
        key_upper = suffix.upper()
        self.DISCORD_WEBHOOK_URL = (
            self.DISCORD_WEBHOOK_URLS.get(suffix)
            or _env(f"DISCORD_WEBHOOK_URL_{key_upper}", required=True)
        )

    # 便利メソッド：任意の環境名でWebhookを取得（未設定なら None）
    def get_webhook(self, env_name: Optional[str] = None) -> Optional[str]:
        if env_name is None:
            return self.DISCORD_WEBHOOK_URL
        return self.DISCORD_WEBHOOK_URLS.get(env_name.lower())

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
