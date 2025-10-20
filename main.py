import sys
from config import Settings
from notion_api import get_notion_database
from process_data import (
    pick_random_unread_title_url,
    pick_random_unread_book,
    pick_random_unread_textbook,
    build_daily_message,
)
from discord_message import send_discord_message

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <env>")
        print("Example: python main.py paper")
        sys.exit(1)

    env_name = sys.argv[1].lower()
    settings = Settings(env_suffix=env_name)

    print(f"[INFO] Running Notion→Discord for env: {env_name}")
    print(f"[INFO] DB ID: {settings.NOTION_DATABASE_ID}")

    results = get_notion_database(
        settings.NOTION_API_KEY,
        settings.NOTION_DATABASE_ID,
        settings.NOTION_VERSION
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

    message = build_daily_message(title, url, settings)
    print(f"[INFO] Generated message:\n{message}")
    send_discord_message(message, settings)
