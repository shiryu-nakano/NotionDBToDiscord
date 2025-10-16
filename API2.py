import requests

def get_notion_database(api_key: str, database_id: str, notion_version: str = "2022-06-28"):
    """
    Notion APIを使用して指定したデータベースの全件（ページネーション対応）を取得します。

    Args:
        api_key (str): Notionの統合トークン。
        database_id (str): 取得対象のデータベースID。
        notion_version (str): 使用するNotion APIのバージョン（デフォルトは "2022-06-28"）。

    Returns:
        list: 取得した全ページ情報のリスト。エラー時は例外を発生させます。
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

def extract_property_(page: dict, property_name: str):
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
    # 他の型も必要に応じて追加できます
    return None

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
    # --- 設定 ---
    NOTION_API_KEY = "your notion api key"         # Notionの統合トークン（ご自身のトークンに置き換えてください）
    DATABASE_ID = "your notion database id"         # 対象のNotionデータベースID（ご自身のデータベースIDに置き換えてください）
    NOTION_VERSION = "2022-06-28"            # 使用するNotion APIのバージョン

    # 取得したいプロパティ名のリスト（例: "Name"と"URL"）
    SELECTED_PROPERTIES = ["Name", "Done","Checkbox"]

    try:
        # データベースの全件を取得
        results = get_notion_database(NOTION_API_KEY, DATABASE_ID, NOTION_VERSION)
        print("Notionデータベースの内容 (全件):\n")
        for idx, page in enumerate(results, start=1):
            formatted_info = format_page_info(page, SELECTED_PROPERTIES)
            print(f"--- Page {idx} ---")
            print(formatted_info)
            print()  # 空行で区切り
    except Exception as e:
        print("エラーが発生しました:", e)
