import requests


def send_discord_message(message: str, webhook: str) -> None:
    resp = requests.post(webhook, json={"content": message})
    if resp.status_code != 204:
        raise RuntimeError(f"Discord送信失敗: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    """
    discordへのメッセージ送信テスト
    DISCORD_WEBHOOK_URL_<ENV>: discordのwebhook→これは.envであらかじめ設定しておくこと

    成功すればdiscordに`test_title`で指定した文字列が送信される

    Usage: python -m send.discord <env_name>
    Example: python -m send.discord paper
    """
    import os
    import sys
    from types import SimpleNamespace

    from dotenv import load_dotenv

    from utils.message import build_daily_message

    load_dotenv()

    env_name = sys.argv[1].lower() if len(sys.argv) >= 2 else "paper"

    print(f"[INFO] Running send.discord test for environment: {env_name}")
    _DISCORD_WEBHOOK_URL = os.getenv(f"DISCORD_WEBHOOK_URL_{env_name.upper()}")
    _MESSAGE_GREETING = os.getenv(f"MESSAGE_GREETING_{env_name.upper()}")
    _settings = SimpleNamespace(MESSAGE_TEMPLATE=os.getenv("MESSAGE_TEMPLATE", "{greeting}\n{title}\n{url}"))

    # 任意のテストメッセージ
    test_title = "これはテストメッセージです！"
    test_url = "https://hackertyper.net/"  # 遊びです．アクセスしてみよう
    message = build_daily_message(test_title, test_url, _settings, _MESSAGE_GREETING)
    send_discord_message(message, _DISCORD_WEBHOOK_URL)
    print("送信成功")
