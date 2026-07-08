import sys

from utils.config import settings, TARGETS
from utils.message import build_daily_message

if __name__ == "__main__":
    # 引数がないと動かない様にしている
    if len(sys.argv) != 2:
        print("Usage: python -m run.notion_db_discord <env>")
        print("Example: python -m run.notion_db_discord paper")
        sys.exit(1)

    env_name = sys.argv[1].lower()

    if env_name not in TARGETS:
        print(f"[ERROR] Unknown env: {env_name}")
        sys.exit(1)

    print(f"[INFO] Running Notion→Discord for env: {env_name}")

    '''
    処理の流れ
    ① target["get"]()  でデータを取得→results
    ② target["pick"](results) でタイトル・URLを取得する
    ③ build_daily_message でmessageを作成する
    ④ target["send"](message, webhook) でmessageをdiscordに送る
    以上
    '''

    target = TARGETS[env_name]

    results = target["get"]()
    title, url = target["pick"](results)
    message = build_daily_message(title, url, settings, target["greeting"])
    print(f"[INFO] Generated message:\n{message}")
    target["send"](message, target["webhook"])
