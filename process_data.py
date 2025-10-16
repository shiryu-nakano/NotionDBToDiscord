
import random
from API2 import extract_property

def get_random_unread_title_url_from_results(results) -> str:
    """
    すでに取得したNotionデータベースのページリスト(results)から、
    'Done' が True ではないページのみを抽出し、未読のものをランダムに1つ選択して
    タイトルとURLを改行でつなげた文字列として返す関数。

    Args:
        results (list): Notion APIで取得したページ情報のリスト。

    Returns:
        str: "タイトル\nURL"の形式の文字列。
             未読のページが存在しない場合は適宜メッセージを返す。
    """
    unread_pages = []
    for page in results:
        done_val = extract_property(page, "Done")  # チェックボックスは "True" or "False" の文字列
        if done_val != "True":
            unread_pages.append(page)

    if not unread_pages:
        return "未読のページはありません。"

    random_page = random.choice(unread_pages)
    title = extract_property(random_page, "Name")
    url = extract_property(random_page, "URL")

    if not title:
        title = "Untitled"
    if not url:
        url = "No URL"

    return f"おはようございます．朝8時です．今日も気張っていきましょう．\n今日の論文は......\n{title}\n{url}"


if __name__ == "__main__":
    from API import get_notion_database

    NOTION_API_KEY = "your notion api"         # Notionの統合トークン（ご自身のトークンに置き換えてください）
    DATABASE_ID = "your notion database id"         # 対象のNotionデータベースID（ご自身のデータベースIDに置き換えてください）
    NOTION_VERSION = "2022-06-28"            # 使用するNotion APIのバージョン

    # 取得したいプロパティ名のリスト（例: "Name"と"URL"）
    SELECTED_PROPERTIES = ["Name", "Done","Checkbox"]

    # すでにNotionからデータベースを取得
    results = get_notion_database(NOTION_API_KEY, DATABASE_ID, NOTION_VERSION)



    # ランダムに未読ページを選択して「タイトル\nURL」を作成
    random_unread_str = get_random_unread_title_url_from_results(results)
    print(random_unread_str)
