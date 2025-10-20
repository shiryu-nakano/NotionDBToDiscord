import sys
from config import settings
from notion_api import get_notion_database
from process_data import (
    pick_random_unread_title_url,
    pick_random_unread_book,
    pick_random_unread_textbook,
    build_daily_message,
)
from discord_message import send_discord_message
import os

if __name__ == "__main__":
    # 引数がないと動かない様にしている
    if len(sys.argv) != 2:
        print("Usage: python main.py <env>")
        print("Example: python main.py paper")
        sys.exit(1)

    env_name = sys.argv[1].lower()
    #settings = Settings(env_suffix=env_name)

    print(f"[INFO] Running Notion→Discord for env: {env_name}")

    '''
    処理の流れ
    ①notion apiでデータを取得→result
    ②process dataでデータを抽出・成形→ pick_random_<>→title,urlを取得する
    ③build daily messageでmessageを作成する
    ④messageをdiscordに送る　
    以上
    '''

    # ⓪ Configを前処理→settingsは不要なので使わない
    _NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    _NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")
    _NOTION_DATABASE_ID = os.getenv(f"NOTION_DATABASE_{env_name.upper()}")
    raw_props = os.getenv(f"SELECTED_PROPERTIES_{env_name.upper()}", "")
    _SELECTED_PROPERTIES = [s.strip() for s in raw_props.split(",") if s.strip()]
    _MESSAGE_GREETING = os.getenv(f"MESSAGE_GREETING_{env_name.upper()}")
    _DISCORD_WEBHOOK_URL = os.getenv(f"DISCORD_WEBHOOK_URL_{env_name.upper()}")


    # ① データ取得
    results = get_notion_database(
        _NOTION_API_KEY,
        _NOTION_DATABASE_ID,
        _NOTION_VERSION
    )

    if env_name == "paper":
        title, url = pick_random_unread_title_url(results)
    elif env_name == "book":
        title, url = pick_random_unread_book(results)
    elif env_name == "academic":
        title, url = pick_random_unread_textbook(results)
    else:
        print(f"[ERROR] Unknown env: {env_name}")
        sys.exit(1)

    message = build_daily_message(title, url, settings, _MESSAGE_GREETING)
    print(f"[INFO] Generated message:\n{message}")
    send_discord_message(message, _DISCORD_WEBHOOK_URL)
