from typing import Any

from pyrogram import filters
from pyrogram.types import InlineQuery, Message

from services import ParseService


async def _platform_filter(_: Any, __: Any, update: Message | InlineQuery) -> bool:
    t: str | None = None
    match update:
        case Message():
            t = update.caption or update.text
        case InlineQuery():
            t = update.query
            
    if not t:
        return False
        
    # ── 【新增：域名白名单拦截】 ──
    # 如果消息里没有包含推特域名，直接返回 False 拒绝触发机器人
    if "x.com" not in t.lower() and "twitter.com" not in t.lower():
        return False

    try:
        return bool(ParseService().parser.get_platform(t))
    except Exception:
        return False


platform_filter = filters.create(_platform_filter)
