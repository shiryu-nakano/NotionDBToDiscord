
import random
from notion_api import extract_property
from config import settings


def pick_random_unread_title_url(results) -> tuple[str,str]:
    """
    すでに取得したNotionデータベースのページリスト(results)から、
    'Done' が True ではないページのみを抽出し、未読のものをランダムに1つ選択して
    タイトルとURLを改行でつなげた文字列として返す関数。

    Args:
        results (list): Notion APIで取得したページ情報のリスト。

    Returns:
        tuple(str,str)
        str: title of the page
        str: url of tha page
    """
    unread = []
    for page in results:
        done = extract_property(page, "Done")  # "True"/"False"/None を返す実装想定
        if done != "True":
            unread.append(page)
    if not unread:
        return ("未読のページはありません。", "")
    p = random.choice(unread)
    title = extract_property(p, "Name")
    url   = extract_property(p, "URL")
    return (title or "Untitled", url or "No URL")

def build_daily_message(title: str, url: str) -> str:
    tpl = settings.MESSAGE_TEMPLATE.replace("\\n", "\n") 
    return tpl.format(
        greeting=settings.MESSAGE_GREETING,
        title=(title or "Untitled"),
        url=(url or "No URL"),
    )



if __name__ == "__main__":
    '''
    連結テスト
    notion_api+process_dataの連結テスト，簡易版

    ① test of notion_api
    envで指定したnotionのAPI，DBのIDを使ってデータベースからページを取得し，
    
    ② test of process_data.pick_random_unread_title_url
    未読のものをランダムに1つ選ぶ→返り値はそのページのタイトルとそのページの論文に対応するurlのタプル

    ③ test of process_data.build_daily_message
    ②で得たタイトルとurlをprocess_dataのbuild_daily_messageに渡してメッセージを作成

    成功すればNotionにある未読の論文のうち1つのタイトルとURLが標準出力される．
    '''

    from notion_api import get_notion_database

    NOTION_API_KEY = settings.NOTION_API_KEY
    DATABASE_ID = settings.NOTION_DATABASE_ID
    NOTION_VERSION = settings.NOTION_VERSION

    # 取得したいプロパティ名のリスト（例: "Name"と"URL"）
    SELECTED_PROPERTIES = settings.SELECTED_PROPERTIES

    # Notionからデータベースを取得
    results = get_notion_database(NOTION_API_KEY, DATABASE_ID, NOTION_VERSION)

    # 未読のものをランダムに1つ選ぶ
    title, url = pick_random_unread_title_url(results)
    print(f"Title: {title}\nURL: {url}")

    # メッセージを作成
    message = build_daily_message(title, url)
    print("\n=== Generated Message ===")
    print(message)
    print("=========================")
