from utils.config import Settings


def build_daily_message(title: str, url: str, settings: Settings, greeting: str) -> str:
    tpl = settings.MESSAGE_TEMPLATE.replace("\\n", "\n")
    return tpl.format(
        greeting=greeting,
        title=(title or "Untitled"),
        url=(url or "No URL"),
    )
