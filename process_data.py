
import random
from notion_api import extract_property
from config import Settings


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


# BOOK
def pick_random_unread_book(results) -> tuple[str,str]:
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
        progress = extract_property(page, "Status")  # "True"/"False"/None を返す実装想定
        #print(f"[DEBUG] Progress status: {progress}")  # デバッグ用出力
        if progress ==  "In progress":
            unread.append(page)
    if not unread:
        return ("未読のページはありません。", "")
    p = random.choice(unread)
    title = extract_property(p, "Name")
    url   = extract_property(p, "Status")
    return (title or "Untitled", url or "No URL")


# TEXTBOOK
def pick_random_unread_textbook(results) -> tuple[str,str]:
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
    booklist = []
    unread = []


    for page in results:
        category = extract_property(page, "Select")
        #print(f"[DEBUG] Page Category : {category}")  # デバッグ用出力
        if category == "Book":
            booklist.append(page)
    if not booklist:
        return ("本が登録されていません。", "")
    #print(f"[DEBUG] Booklist Length : {booklist[0]}")  # デバッグ用出力
    
    for page in booklist:
        status = extract_property(page, "Status")  # "True"/"False"/None を返す実装想定
        #print(f"[DEBUG] Status: {status}")  # デバッグ用出力
        if status == "In progress":
            unread.append(page)
    if not unread:
        return ("未読のページはありません。", "")
    p = random.choice(unread)
    title = extract_property(p, "Name")
    url   = extract_property(p, "URL")
    return (title or "Untitled", url or "No URL")







def build_daily_message(title: str, url: str, settings:Settings) -> str:
    tpl = settings.MESSAGE_TEMPLATE.replace("\\n", "\n") 
    return tpl.format(
        greeting=settings.MESSAGE_GREETING,
        title=(title or "Untitled"),
        url=(url or "No URL"),
    )


if __name__ == "__main__":
    import sys
    from notion_api import get_notion_database
    from config import Settings

    if len(sys.argv) != 2:
        print("Usage: python process_data.py <env_name>")
        print("Example: python process_data.py paper")
        sys.exit(1)

    env_name = sys.argv[1].lower()
    settings = Settings(env_suffix=env_name)

    print(f"[INFO] Running process_data test for environment: {env_name}")
    print(f"[INFO] Using database: {settings.NOTION_DATABASE_ID}")

    # Notionからデータベースを取得
    results = get_notion_database(
        settings.NOTION_API_KEY,
        settings.NOTION_DATABASE_ID,
        settings.NOTION_VERSION
    )

    # 選択する関数を環境ごとに分岐
    if env_name == "paper":
        title, url = pick_random_unread_title_url(results)
    elif env_name == "book":
        title, url = pick_random_unread_book(results)
    elif env_name == "academic":
        title, url = pick_random_unread_textbook(results)
    else:
        print(f"[ERROR] Unknown environment name: {env_name}")
        sys.exit(1)

    # メッセージ作成
    message = build_daily_message(title, url, settings)
    print("\n=== Generated Message ===")
    print(message)
    print("=========================")
