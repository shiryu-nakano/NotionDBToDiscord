import random


def pick_unsolved_problem(results: tuple, levels: list, exclude_prefixes: list) -> tuple[str, str]:
    """
    get.atcoder.get_atcoder_unsolved_candidates() の返り値 (problems, ac_ids) から、
    levels に一致し、かつAC済みでない問題をランダムに1問選択して
    タイトルとURLのタプルとして返す。

    Args:
        results (tuple): (problems: list, ac_ids: set)
        levels (list): 対象とする問題番号(A/Bなど)のリスト。
        exclude_prefixes (list): 除外したいコンテストIDの接頭辞のリスト。

    Returns:
        tuple(str, str): (title, url)
    """
    problems, ac_ids = results
    candidates = [
        p
        for p in problems
        if p["problem_index"].upper() in levels
        and p["id"] not in ac_ids
        and not any(p["contest_id"].startswith(pref) for pref in exclude_prefixes)
    ]
    if not candidates:
        return (f"Level {'/'.join(levels)} の問題は全てAC済みです！おめでとうございます🎉", "")

    problem = random.choice(candidates)
    title = f"[{problem['problem_index']}] {problem['title']}"
    url = f"https://atcoder.jp/contests/{problem['contest_id']}/tasks/{problem['id']}"
    return (title, url)



if __name__ == "__main__":
    # デバッグ用
    from get.atcoder import get_atcoder_unsolved_candidates
    from utils.config import get_atcoder_target

    settings, _ = get_atcoder_target()
    results = get_atcoder_unsolved_candidates(
        settings.ATCODER_USER_ID, settings.ATCODER_CACHE_PATH
    )
    title, url = pick_unsolved_problem(results, ["A", "B"], ["abc"])
    print(f"title: {title}")
    print(f"url: {url}")