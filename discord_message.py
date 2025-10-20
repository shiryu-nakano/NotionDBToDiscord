from config import settings
import requests


def send_discord_message(message: str, webhook:str) -> None:
    resp = requests.post(webhook, json={"content": message})
    if resp.status_code != 204:
        raise RuntimeError(f"Discord送信失敗: {resp.status_code} {resp.text}")


# settingなんていらないstrで十分

if __name__ == "__main__":
    '''
    discordへのメッセージ送信テスト
    DISCORD_WEBHOOK_URL: discordのwebhook→これは.evnであらかじめ設定しておくこと

    成功すればdiscordに`test_message`で指定した文字列が送信される
    '''
    import sys
    from config import Settings
    from process_data import build_daily_message
    import os

    env_name = sys.argv[1].lower() if len(sys.argv) >= 2 else "paper"
    #settings = Settings(env_suffix=env_name)

    print(f"[INFO] Running process_data test for environment: {env_name}")
    _DISCORD_WEBHOOK_URL = os.getenv(f"DISCORD_WEBHOOK_URL_{env_name.upper()}")
    _MESSAGE_GREETING = os.getenv(f"MESSAGE_GREETING_{env_name.upper()}")
    
    # 任意のテストメッセージ
    test_title = "これはテストメッセージです！"
    test_url = "https://hackertyper.net/" # 遊びです．アクセスしてみよう
    message = build_daily_message(test_title, test_url, settings,_MESSAGE_GREETING)
    send_discord_message(message, _DISCORD_WEBHOOK_URL)
    print("送信成功")
    # 送信内容を標準出力す
    
    

