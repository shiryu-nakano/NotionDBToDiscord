from dotenv import load_dotenv
import os
from typing import Optional

'''
.env で設定した変数を読み込んで，設定クラスに格納する

対象(Notion系/AtCoder)ごとに独立したSettingsクラスを用意し、
get_notion_targets()/get_atcoder_target() が呼ばれた時にだけ、
その対象に必要な環境変数を検証する。
こうすることで、例えば run/atcoder_discord.py はNotion関連の
環境変数が一切無くても単体で動作できる。
'''


load_dotenv()


def _env(name: str, default: Optional[str] = None, required: bool = False) -> str:
    val = os.getenv(name, default)
    if required and not val:
        raise RuntimeError(f"Environment variable '{name}' is required but not set")
    return val


class NotionSettings:
    def __init__(self):
        # Common
        self.NOTION_API_KEY = _env("NOTION_API_KEY", required=True)
        self.NOTION_VERSION = _env("NOTION_VERSION", "2022-06-28")
        self.MESSAGE_TEMPLATE = _env("MESSAGE_TEMPLATE", "{greeting}\n{title}\n{url}")

        # Paper
        self.NOTION_DATABASE_PAPER = _env("NOTION_DATABASE_PAPER", required=True)
        self.DISCORD_WEBHOOK_URL_PAPER = _env("DISCORD_WEBHOOK_URL_PAPER", required=True)
        self.MESSAGE_GREETING_PAPER = _env("MESSAGE_GREETING_PAPER", "おはようございます．今日の論文は.....")
        self.SELECTED_PROPERTIES_PAPER = [s.strip() for s in _env("SELECTED_PROPERTIES_PAPER", "Name,Done,URL").split(",")]

        # Book
        self.NOTION_DATABASE_BOOK = _env("NOTION_DATABASE_BOOK", required=True)
        self.DISCORD_WEBHOOK_URL_BOOK = _env("DISCORD_WEBHOOK_URL_BOOK", required=True)
        self.MESSAGE_GREETING_BOOK = _env("MESSAGE_GREETING_BOOK", "おはようございます．今日の本は.....")
        self.SELECTED_PROPERTIES_BOOK = [s.strip() for s in _env("SELECTED_PROPERTIES_BOOK", "Name,Status,chps").split(",")]

        # Textbook
        self.NOTION_DATABASE_ACADEMIC = _env("NOTION_DATABASE_ACADEMIC", required=True)
        self.DISCORD_WEBHOOK_URL_ACADEMIC = _env("DISCORD_WEBHOOK_URL_ACADEMIC", required=True)
        self.MESSAGE_GREETING_ACADEMIC = _env("MESSAGE_GREETING_ACADEMIC", "おはようございます．今日の教科書は.....")
        self.SELECTED_PROPERTIES_ACADEMIC = [s.strip() for s in _env("SELECTED_PROPERTIES_ACADEMIC", "Name,Status,Select").split(",")]

    def __repr__(self):
        masked = lambda s: (s[:8] + "..." + s[-4:]) if s and len(s) > 20 else (s or "")
        return (
            "NotionSettings(\n"
            f"  NOTION_API_KEY: {masked(self.NOTION_API_KEY)}\n"
            f"  NOTION_DATABASE_PAPER: {self.NOTION_DATABASE_PAPER}\n"
            f"  DISCORD_WEBHOOK_URL_PAPER: {masked(self.DISCORD_WEBHOOK_URL_PAPER)}\n"
            f"  NOTION_DATABASE_BOOK: {self.NOTION_DATABASE_BOOK}\n"
            f"  DISCORD_WEBHOOK_URL_BOOK: {masked(self.DISCORD_WEBHOOK_URL_BOOK)}\n"
            f"  NOTION_DATABASE_ACADEMIC: {self.NOTION_DATABASE_ACADEMIC}\n"
            f"  DISCORD_WEBHOOK_URL_ACADEMIC: {masked(self.DISCORD_WEBHOOK_URL_ACADEMIC)}\n"
            )


class AtcoderSettings:
    def __init__(self):
        self.MESSAGE_TEMPLATE = _env("MESSAGE_TEMPLATE", "{greeting}\n{title}\n{url}")

        self.ATCODER_USER_ID = _env("ATCODER_USER_ID", required=True)
        self.ATCODER_LEVELS = ["A","B"] #[s.strip().upper() for s in _env("ATCODER_LEVELS", "A").split(",") if s.strip()]
        self.ATCODER_EXCLUDE_PREFIXES = [s.strip() for s in _env("ATCODER_EXCLUDE_PREFIXES", "").split(",") if s.strip()]
        self.ATCODER_CACHE_PATH = _env("ATCODER_CACHE_PATH", "data/ac_cache.json")
        self.DISCORD_WEBHOOK_URL_ATCODER = _env("DISCORD_WEBHOOK_URL_ATCODER", required=True)
        self.MESSAGE_GREETING_ATCODER = "おはようございます．今日のAtCoderの問題は....." # _env("MESSAGE_GREETING_ATCODER", "おはようございます．今日のAtCoderの問題は.....")

    def __repr__(self):
        masked = lambda s: (s[:8] + "..." + s[-4:]) if s and len(s) > 20 else (s or "")
        return (
            "AtcoderSettings(\n"
            f"  ATCODER_USER_ID: {self.ATCODER_USER_ID}\n"
            f"  ATCODER_LEVELS: {self.ATCODER_LEVELS}\n"
            f"  DISCORD_WEBHOOK_URL_ATCODER: {masked(self.DISCORD_WEBHOOK_URL_ATCODER)}\n"
            )


def get_notion_targets() -> tuple[NotionSettings, dict]:
    """
    Notion由来の対象(paper/book/academic)ごとに、どのget/pick/sendの組み合わせを使うか、
    そしてどの設定値(DB ID・Webhook URL・挨拶文)を使うかを定義する。
    NotionSettings() はここで初めてインスタンス化されるため、
    Notion関連の環境変数が揃っていない場合、このタイミングで初めてエラーになる。

    run/notion_db_discord.py はこの関数を呼ぶだけで処理を実行できる。
    """
    from get.notion import get_notion_database
    from pick.random import (
        pick_random_unread_title_url,
        pick_random_unread_book,
        pick_random_unread_textbook,
    )
    from send.discord import send_discord_message

    settings = NotionSettings()

    targets = {
        "paper": {
            "get": lambda: get_notion_database(
                settings.NOTION_API_KEY, settings.NOTION_DATABASE_PAPER, settings.NOTION_VERSION
            ),
            "pick": pick_random_unread_title_url,
            "send": send_discord_message,
            "webhook": settings.DISCORD_WEBHOOK_URL_PAPER,
            "greeting": settings.MESSAGE_GREETING_PAPER,
        },
        "book": {
            "get": lambda: get_notion_database(
                settings.NOTION_API_KEY, settings.NOTION_DATABASE_BOOK, settings.NOTION_VERSION
            ),
            "pick": pick_random_unread_book,
            "send": send_discord_message,
            "webhook": settings.DISCORD_WEBHOOK_URL_BOOK,
            "greeting": settings.MESSAGE_GREETING_BOOK,
        },
        "academic": {
            "get": lambda: get_notion_database(
                settings.NOTION_API_KEY, settings.NOTION_DATABASE_ACADEMIC, settings.NOTION_VERSION
            ),
            "pick": pick_random_unread_textbook,
            "send": send_discord_message,
            "webhook": settings.DISCORD_WEBHOOK_URL_ACADEMIC,
            "greeting": settings.MESSAGE_GREETING_ACADEMIC,
        },
    }
    return settings, targets


def get_atcoder_target() -> tuple[AtcoderSettings, dict]:
    """
    AtCoder向けのget/pick/sendの組み合わせを定義する。
    AtcoderSettings() はここで初めてインスタンス化されるため、
    Notion関連の環境変数が無くても、AtCoder関連さえ揃っていれば動作する。

    run/atcoder_discord.py はこの関数を呼ぶだけで処理を実行できる。
    """
    from get.atcoder import get_atcoder_unsolved_candidates
    from pick.atcoder import pick_unsolved_problem
    from send.discord import send_discord_message

    settings = AtcoderSettings()

    # envの初期設定を使わずに，greeting と　levelを指定する
    '''
    target = {
        "get": lambda: get_atcoder_unsolved_candidates(
            settings.ATCODER_USER_ID, settings.ATCODER_CACHE_PATH
        ),
        "pick": lambda results: pick_unsolved_problem(
            results, settings.ATCODER_LEVELS, settings.ATCODER_EXCLUDE_PREFIXES
        ),
        "send": send_discord_message,
        "webhook": settings.DISCORD_WEBHOOK_URL_ATCODER,
        "greeting": settings.MESSAGE_GREETING_ATCODER,
    }
    '''
    target = {
        "get": lambda: get_atcoder_unsolved_candidates(
            settings.ATCODER_USER_ID, settings.ATCODER_CACHE_PATH
        ),
        "pick": lambda results: pick_unsolved_problem(
            results, ["A", "B"], settings.ATCODER_EXCLUDE_PREFIXES
        ),
        "send": send_discord_message,
        "webhook": settings.DISCORD_WEBHOOK_URL_ATCODER,
        "greeting": "おはようございます．今日のAtCoderの問題は.....",
    }
    return settings, target


if __name__ == "__main__":
    try:
        settings, _ = get_notion_targets()

        print("\n\n=== .env テスト出力 (Notion) ===")
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
        print("\n[エラー] Notion設定を読み込めませんでした。")
        print(e)
        print(".envファイルの内容を確認してください。")

    try:
        settings, _ = get_atcoder_target()

        print("\n\n=== .env テスト出力 (AtCoder) ===")
        print(settings)
        print("========================")

    except RuntimeError as e:
        print("\n[エラー] AtCoder設定を読み込めませんでした。")
        print(e)
        print(".envファイルの内容を確認してください。")
