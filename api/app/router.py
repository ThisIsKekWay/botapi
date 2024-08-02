import json

from fastapi import APIRouter, Request
from fastapi_versioning import version
from app.database import msg_dao as dao
from app.misc import redis

router = APIRouter(
    tags=['Messages'],
    prefix=''
)


@router.get('/messages')
@version(1)
async def get_messages(request: Request, page: int = 1):
    page_size = 10
    formatted_msgs = []
    cached_messages = await redis.get(f'cached_messages_page_{page}')
    if cached_messages:
        cached_messages = json.loads(cached_messages.decode('utf-8'))
    else:
        cached_messages = []
        msgs = await dao.get_msg_with_pagination(page, page_size)
        page = msgs[0].get("page")
        for message in msgs[1:]:
            message.pop("_id", None)
            formatted_msg = {'Author ID': message['author_tg_id'], 'Text': message['text']}
            cached_messages.append(formatted_msg)
        formatted_msgs_str = json.dumps(cached_messages)
        await redis.set(f'cached_messages_page_{page}', formatted_msgs_str)
    return cached_messages


@router.post('/message')
@version(1)
async def post_message(request: Request, text: str):
    data = {"author_tg_id": "Unknown", "text": text}
    await dao.insert(data)
    cache = await redis.keys("*")
    if cache:
        last_key = max(cache).decode("utf-8")
        last_cache = await redis.get(last_key)
        if len(json.loads(last_cache.decode('utf-8'))) < 10:
            await redis.delete(last_key)

    return {"status": "OK", 'text': text}
