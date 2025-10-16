from config import settings
from notion_api import *
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
    NOTION_API_KEY = settings.NOTION_API_KEY       
    DATABASE_ID = settings.NOTION_DATABASE_ID     
    NOTION_VERSION = settings.NOTION_VERSION  
    DISCORD_WEBHOOK_URL = settings.DISCORD_WEBHOOK_URL   

    # 取得したいプロパティ名のリスト
    SELECTED_PROPERTIES = settings.SELECTED_PROPERTIES

    # Notionからデータベースを取得
    results = get_notion_database(NOTION_API_KEY, DATABASE_ID, NOTION_VERSION)

    # ランダムに未読ページを選択し
    title, url = pick_random_unread_title_url(results)
    message = build_daily_message(title, url)
    send_discord_message(message)
    print("\n[LOG]-------------------------------")
    print("送信したメッセージ:")    
    print(message)
    print("[LOG]-------------------------------\n")
    
