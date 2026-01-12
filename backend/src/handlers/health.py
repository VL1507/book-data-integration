from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working"}


@router.get("/ping")
async def ping_pong():
    return {"ping": "pong!"}
