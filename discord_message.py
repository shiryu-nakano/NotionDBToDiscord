import requests

def send_discord_message(message: str, webhook_url: str):
    """
    DiscordのWebhookを使用して指定したメッセージを送信する

    Args:
        message (str): 送信するメッセージの文字列
        webhook_url (str): DiscordのWebhook URL
    """
    payload = {
        "content": message
    }
    response = requests.post(webhook_url, json=payload)
    
    # DiscordのWebhookは成功時に204(No Content)を返すためそれをチェックする
    if response.status_code != 204:
        raise Exception(f"Discordへのメッセージ送信に失敗しました。レスポンス: {response.text}")
    
    print("Discordへのメッセージ送信に成功しました。")

if __name__ == "__main__":
    # --- 設定 ---
    # ご自身のDiscordのWebhook URLに置き換えてください
    DISCORD_WEBHOOK_URL = "your discord webhook"
    
    # 任意のテストメッセージ
    test_message = "これはテストメッセージです！"
    
    send_discord_message(test_message, DISCORD_WEBHOOK_URL)
