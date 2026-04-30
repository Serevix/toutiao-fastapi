from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

#数据库URL
ASYNC_DATABASE_URL="mysql+aiomysql://root:!Hkd213717@localhost:3306/news_app?charset=utf8mb4"

#创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo= True,         #输出SQL日志
    pool_size=10,       #连接池大小
    pool_recycle=3600,  #连接池回收时间
    max_overflow=20      #设置连接池上溢数量
)
#创建异步会话工厂
AsyncSessionLocal=async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,#指定 async_sessionmaker 创建的会话对象的类型
    expire_on_commit=False
)

#依赖项。用于获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()