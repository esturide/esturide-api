from fastapi import APIRouter

root = APIRouter(
    tags=["Root"]
)


@root.get('/')
async def index():
    return {
        "status": "ok",
    }
