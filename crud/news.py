"""
数据库的增删改查
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category,News

async def get_categories(db:AsyncSession,skip:int=0,limit:int=10):
    stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    #查询指定分类下的新闻
    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int):
    stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(stmt)
    return result.scalar_one()  #只能有一个结果，否则报错

async def get_news_detail(db:AsyncSession,news_id:int):
    result=await db.execute(select(News).where(News.id==news_id))
    return result.scalar_one_or_none()

async def increase_news_views(db:AsyncSession,news_id:int):
    stmt=update(News).where(News.id==news_id).values(views=News.views+1)
    result=await db.execute(stmt)
    await db.commit()
    #需要检查数据库是否真的命中了数据
    return result.rowcount > 0 #rowcount表示受影响的行数

async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit:int=5):
    #
    stmt=select(News).where(
        News.id!=news_id,
        News.category_id==category_id
    ).orderby(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result=await db.execute(stmt)
    # return result.scalars().all()
    related_news=result.scalars().all()
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "description": news_detail.description,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "category_id": news_detail.category_id,
        "views": news_detail.views,
    } for news_detail in related_news]