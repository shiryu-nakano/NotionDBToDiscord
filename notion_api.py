from config import settings
import requests

def get_notion_database(api_key: str, database_id: str, notion_version: str = "2022-06-28"):
    """
    Notion APIを使用して指定したデータベースの全件を取得する

    Args:
        api_key (str): Notionの統合トークン。
        database_id (str): 取得対象のデータベースID。
        notion_version (str): 使用するNotion APIのバージョン（デフォルトは "2022-06-28"）。

    Returns:
        list: 取得した全ページ情報のリスト。エラー時は例外を発生させます
    """

    notion_api_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": notion_version,
        "Content-Type": "application/json",
    }

    all_results = []
    start_cursor = None

    while True:
        payload = {}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = requests.post(notion_api_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception("Notion APIからデータを取得できませんでした。", response.text)

        data = response.json()
        results = data.get("results", [])
        all_results.extend(results)

        if not data.get("has_more", False):
            break
        start_cursor = data.get("next_cursor")
    
    if not all_results:
        raise Exception("データベースにページが存在しません。")
    
    return all_results


def extract_property(page: dict, property_name: str):
    """
    指定したプロパティの値をページから抽出します。
    
    Args:
        page (dict): Notion APIから取得したページ情報。
        property_name (str): 取得対象のプロパティ名。

    Returns:
        str: 抽出した値（文字列）。プロパティが存在しない場合はNoneを返します。
    """
    properties = page.get("properties", {})
    if property_name not in properties:
        return None

    prop = properties[property_name]
    prop_type = prop.get("type")
    #print(f"[DEBUG] Extracting property '{property_name}' of type '{prop_type}'")  # デバッグ用出力

    if prop_type == "title":
        # タイトルの場合、複数のテキストブロックを結合
        return "".join([t.get("plain_text", "") for t in prop.get("title", [])])
    elif prop_type == "url":
        return prop.get("url")
    elif prop_type == "rich_text":
        return "".join([t.get("plain_text", "") for t in prop.get("rich_text", [])])
    elif prop_type == "number":
        return str(prop.get("number"))
    elif prop_type == "select":
        option = prop.get("select")
        return option.get("name") if option else ""
    elif prop_type == "date":
        date_info = prop.get("date")
        return date_info.get("start") if date_info else ""
    elif prop_type == "checkbox":
        # チェックボックスはbooleanで返るので、文字列に変換して返す
        return str(prop.get("checkbox"))
    elif prop_type == "status":
        status_info = prop.get("status")
        return status_info.get("name") if status_info else None
    # 他の型も必要に応じて追加できます
    return None


def format_page_info(page: dict, selected_properties: list):
    """
    指定したプロパティのみを抽出し、見やすく改行付きの文字列に整形します。
    
    Args:
        page (dict): Notion APIから取得したページ情報。
        selected_properties (list): 取得したいプロパティ名のリスト。

    Returns:
        str: 整形済みのページ情報。
    """
    lines = []
    lines.append(f"Page ID: {page.get('id')}")
    for prop in selected_properties:
        value = extract_property(page, prop)
        lines.append(f"{prop}: {value}")
    return "\n".join(lines)

if __name__ == "__main__":
    import os
    import sys
    from dotenv import load_dotenv

    load_dotenv()

    # 実行引数からターゲット環境名を取得
    if len(sys.argv) != 2:
        print("Usage: python notion_api.py <env_name>")
        print("Example: python notion_api.py paper")
        sys.exit(1)

    env_name = sys.argv[1].lower()

    # 共通設定
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")

    # サフィックス付き変数を取得    
    NOTION_DATABASE_ID = os.getenv(f"NOTION_DATABASE_{env_name.upper()}")
    raw_props = os.getenv(f"SELECTED_PROPERTIES_{env_name.upper()}", "")
    SELECTED_PROPERTIES = [s.strip() for s in raw_props.split(",") if s.strip()]

    if not NOTION_DATABASE_ID:
        raise RuntimeError(f"NOTION_DATABASE_{env_name} が設定されていません")
    if not SELECTED_PROPERTIES:
        raise RuntimeError(f"SELECTED_PROPERTIES_{env_name} が設定されていません")

    # データベース取得
    try:
        results = get_notion_database(NOTION_API_KEY, NOTION_DATABASE_ID, NOTION_VERSION)
        print(f"\n[INFO] Notion DB test for environment: {env_name}")
        print(f"[INFO] Database ID: {NOTION_DATABASE_ID}")
        print(f"[INFO] Selected properties: {SELECTED_PROPERTIES}")
        print("\n=== First 5 entries ===")

        for i, page in enumerate(results[:5]):
            print(f"--- Page {i+1} ---")
            for prop in SELECTED_PROPERTIES:
                val = extract_property(page, prop)
                print(f"{prop}: {val}")
            print()

    except Exception as e:
        print("エラーが発生しました:", e)