from utils.config import get_atcoder_target
from utils.message import build_daily_message

if __name__ == "__main__":
    print("[INFO] Running AtCoder→Discord")

    '''
    処理の流れ
    ① target["get"]()  でデータを取得→results
    ② target["pick"](results) でタイトル・URLを取得する
    ③ build_daily_message でmessageを作成する
    ④ target["send"](message, webhook) でmessageをdiscordに送る
    以上
    '''

    settings, target = get_atcoder_target()
    print("======= Basic Configuration =======")
    print(f"[INFO] Script path: {__file__}")
    print(f"[INFO] AtCoder user ID: {settings.ATCODER_USER_ID}")
    print(f"[INFO] AtCoder levels: {settings.ATCODER_LEVELS}")
    print(f"[INFO] AtCoder exclude prefixes: {settings.ATCODER_EXCLUDE_PREFIXES}")
    print(f"[INFO] Discord webhook URL: {settings.DISCORD_WEBHOOK_URL_ATCODER}")
    print(f"[INFO] Message greeting: {settings.MESSAGE_GREETING_ATCODER}")
    print(f"[INFO] Message template: {settings.MESSAGE_TEMPLATE}")
    
    if len(settings.ATCODER_LEVELS) == 2 :
        print("============== Process ===============")
        from pick.atcoder import pick_unsolved_problem
        from utils.config import get_atcoder_target
        from utils.message import build_daily_message
        
        results = target["get"]()
        print(f"[INFO] Retrieved {len(results[0])} problems, {len(results[1])} AC IDs")
        picks: list[tuple[str, str]] = [
            pick_unsolved_problem(results, [level], settings.ATCODER_EXCLUDE_PREFIXES)
            for level in settings.ATCODER_LEVELS
            ]
        print(f"[INFO] Picked problems: {picks}")

        lines = []
        progress:str = f"今の所あなたは{len(results[1])}問をAC済みです！" if len(results[1]) > 0 else "まだ問題がありません。"
        for title, url in picks:
            lines.append(f"{title}\n{url}")
        lines.append(progress)
        combined_body = "\n\n".join(lines)
        message = f"\nこんにちは\n{target['greeting']}\n{combined_body}"
        target["send"](message, target["webhook"])
        print("========== Message ===========")
        print(f"{message}")
        print("==============================")
        
    else:
        results = target["get"]()
        print(f"[INFO] Retrieved {len(results[0])} problems, {len(results[1])} AC IDs")

        title, url = target["pick"](results)
        print(f"[INFO] Picked problem: {title} ({url})")

        print("======= Message =======")
        message = build_daily_message(title, url, settings, target["greeting"])
        print(f"{message}")
        #target["send"](message, target["webhook"])
        print("=======================")

    print("[INFO][DONE] AtCoder→Discord process completed.")

    




