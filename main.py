from API import *
import random
from  discord_message import *
from process_data import *

if __name__ == "__main__":
    '''
    連結テスト
    ①NotionのDBから未読の論文を1つランダムに選ぶ

    ②選んだ論文をdiscordに送る

    成功すればNotionにある未読の論文のうち1つがDiscordにメッセージとして送られる．

    '''

    # --- 設定 ---
    NOTION_API_KEY = "your notion api key"         # Notionの統合トークン（ご自身のトークンに置き換えてください）
    DATABASE_ID = "your notion database id"         # 対象のNotionデータベースID（ご自身のデータベースIDに置き換えてください）
    NOTION_VERSION = "2022-06-28"            # 使用するNotion APIのバージョン

    # 取得したいプロパティ名のリスト（例: "Name"と"URL"）
    SELECTED_PROPERTIES = ["Name", "Done", "URL"]

    # すでにNotionからデータベースを取得
    results = get_notion_database(NOTION_API_KEY, DATABASE_ID, NOTION_VERSION)



    # ランダムに未読ページを選択して「タイトル\nURL」を作成
    random_unread_str = get_random_unread_title_url_from_results(results)
    print(random_unread_str)

    DISCORD_WEBHOOK_URL = "your discord webhook url" 
    # 任意のテストメッセージ
    test_message = random_unread_str
    
    send_discord_message(test_message, DISCORD_WEBHOOK_URL)
