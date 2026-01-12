import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from settings import settings

print(settings)


app = FastAPI(title="Book API", description="API для работы с книгами")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.APP.FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working"}


@app.get("/ping")
async def ping_pong():
    return {"ping": "pong!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP.PORT)
