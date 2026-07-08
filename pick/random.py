import random

from get.notion import extract_property, get_notion_database


def pick_random_unread_title_url(results) -> tuple[str, str]:
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
    url = extract_property(p, "URL")
    return (title or "Untitled", url or "No URL")


# BOOK
def pick_random_unread_book(results) -> tuple[str, str]:
    """
    すでに取得したNotionデータベースのページリスト(results)から、
    'Status' が 'In progress' のページのみを抽出し、未読のものをランダムに1つ選択して
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
        progress = extract_property(page, "Status")
        if progress == "In progress":
            unread.append(page)
    if not unread:
        return ("未読のページはありません。", "")
    p = random.choice(unread)
    title = extract_property(p, "Name")
    url = extract_property(p, "Status")
    return (title or "Untitled", url or "No URL")


# TEXTBOOK
def pick_random_unread_textbook(results) -> tuple[str, str]:
    """
    すでに取得したNotionデータベースのページリスト(results)から、
    'Select' が 'Book' かつ 'Status' が 'In progress' のページのみを抽出し、
    未読のものをランダムに1つ選択してタイトルとURLを改行でつなげた文字列として返す関数。

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
        if category == "Book":
            booklist.append(page)
    if not booklist:
        return ("本が登録されていません。", "")

    for page in booklist:
        status = extract_property(page, "Status")
        if status == "In progress":
            unread.append(page)
    if not unread:
        return ("未読のページはありません。", "")
    p = random.choice(unread)
    title = extract_property(p, "Name")
    url = extract_property(p, "Status")
    return (title or "Untitled", url or "No URL")


if __name__ == "__main__":
    import os
    import sys

    from dotenv import load_dotenv

    load_dotenv()

    if len(sys.argv) != 2:
        print("Usage: python -m pick.random <env_name>")
        print("Example: python -m pick.random paper")
        sys.exit(1)

    env_name = sys.argv[1].lower()
    print(f"[INFO] Running pick.random test for environment: {env_name}")

    _NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    _NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")
    _NOTION_DATABASE_ID = os.getenv(f"NOTION_DATABASE_{env_name.upper()}")

    results = get_notion_database(_NOTION_API_KEY, _NOTION_DATABASE_ID, _NOTION_VERSION)

    if env_name == "paper":
        title, url = pick_random_unread_title_url(results)
    elif env_name == "book":
        title, url = pick_random_unread_book(results)
    elif env_name == "academic":
        title, url = pick_random_unread_textbook(results)
    else:
        print(f"[ERROR] Unknown environment name: {env_name}")
        sys.exit(1)

    print("\n=== Picked ===")
    print(f"title: {title}")
    print(f"url: {url}")
