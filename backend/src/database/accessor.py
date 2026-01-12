from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from settings import settings

engine = create_async_engine(
    url=settings.DB.URL,
    echo=True,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db_session():
    async with AsyncSessionFactory() as session:
        yield session
