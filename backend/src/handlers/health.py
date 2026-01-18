from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "message": "API is working"}


@router.get("/ping")
async def ping_pong() -> dict[str, str]:
    return {"ping": "pong!"}
