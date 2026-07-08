from typing import Protocol


class HasMessageTemplate(Protocol):
    MESSAGE_TEMPLATE: str


def build_daily_message(title: str, url: str, settings: HasMessageTemplate, greeting: str) -> str:
    tpl = settings.MESSAGE_TEMPLATE.replace("\\n", "\n")
    return tpl.format(
        greeting=greeting,
        title=(title or "Untitled"),
        url=(url or "No URL"),
    )
