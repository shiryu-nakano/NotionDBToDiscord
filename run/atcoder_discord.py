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

    results = target["get"]()
    title, url = target["pick"](results)
    message = build_daily_message(title, url, settings, target["greeting"])
    print(f"[INFO] Generated message:\n{message}")
    target["send"](message, target["webhook"])
