import json
import os
import time

import requests

BASE = "https://kenkoooo.com/atcoder"
PROBLEMS_URL = f"{BASE}/resources/problems.json"
SUBMISSIONS_URL = f"{BASE}/atcoder-api/v3/user/submissions"

# AtCoder Problems API のマナーとして、連続アクセス時は1秒以上あける
REQUEST_INTERVAL_SEC = 2.0


def _fetch_json(url: str):
    resp = requests.get(url, headers={"User-Agent": "NotionDBToDiscord/1.0"}, timeout=30)
    if resp.status_code != 200:
        raise Exception("AtCoder APIからデータを取得できませんでした。", resp.status_code, resp.text)
    return resp.json()


def _load_cache(path: str, user_id: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            cache = json.load(f)
        if cache.get("user_id") == user_id:
            return cache
    return {"user_id": user_id, "last_epoch_second": 0, "ac_problem_ids": []}


def _save_cache(path: str, cache: dict):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_atcoder_unsolved_candidates(user_id: str, cache_path: str) -> tuple[list, set]:
    """
    AtCoder Problemsの公開APIから全問題一覧と、指定ユーザーのAC済み問題ID集合を取得する。

    提出履歴は cache_path に「どこまで取得したか(last_epoch_second)」と
    「これまでにACした問題ID一覧」をキャッシュし、2回目以降は差分だけ取得する。

    Args:
        user_id (str): AtCoder Problems 上のユーザーID。
        cache_path (str): AC済みキャッシュファイルのパス。

    Returns:
        tuple(list, set): (全問題のリスト, AC済み問題IDの集合)
    """
    problems = _fetch_json(PROBLEMS_URL)
    time.sleep(REQUEST_INTERVAL_SEC)

    cache = _load_cache(cache_path, user_id)
    ac_ids = set(cache["ac_problem_ids"])
    from_second = cache["last_epoch_second"]

    while True:
        url = f"{SUBMISSIONS_URL}?user={user_id}&from_second={from_second}"
        submissions = _fetch_json(url)
        if not submissions:
            break
        for sub in submissions:
            if sub.get("result") == "AC":
                ac_ids.add(sub["problem_id"])
            from_second = max(from_second, sub["epoch_second"] + 1)
        if len(submissions) < 500:
            break
        time.sleep(REQUEST_INTERVAL_SEC)

    cache["ac_problem_ids"] = sorted(ac_ids)
    cache["last_epoch_second"] = from_second
    _save_cache(cache_path, cache)

    return problems, ac_ids


if __name__ == "__main__":
    import sys

    from dotenv import load_dotenv

    load_dotenv()

    user_id = os.getenv("ATCODER_USER_ID")
    cache_path = os.getenv("ATCODER_CACHE_PATH", "data/ac_cache.json")

    if not user_id:
        print("Usage: ATCODER_USER_ID=<id> python -m get.atcoder")
        sys.exit(1)

    problems, ac_ids = get_atcoder_unsolved_candidates(user_id, cache_path)
    print(f"[INFO] problems: {len(problems)}件, AC済み: {len(ac_ids)}件")
