from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import news
from config.db_config import get_db
#创建APIRouter实例
router=APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(skip:int=0,limit:int=10,db:AsyncSession=Depends(get_db)):
    #获取数据库中的新闻分类
    categories =await news.get_categories(db,skip,limit)
    return {
        "code":200,
        "message":"success",
        "data":categories
    }

@router.get("/list")
async def get_news_list(
        category_id:int=Query(None,description="新闻分类ID",alias="categoryId"),
        page:int=1,
        page_size:int=Query(10,description="每页数量",alias="pageSize",le=100),
        db:AsyncSession=Depends(get_db)):
    offset=(page-1)*page_size
    news_list=await news.get_news_list(db,category_id,offset,page_size)
    total=await news.get_news_count(db,category_id)
    has_more=(offset+len(news_list))<total

    return {
        "code":200,
        "message":"success",
        "data":{
            "List":news_list,
            "total":total,
            "hasMore":has_more
        }
    }

@router.get("/detail")
async def get_news_detail(news_id:int=Query(None,alias="id"),db:AsyncSession=Depends(get_db)):
    #获取新闻详情
    news_detail=await news.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")
    views_res=await news.increase_news_views(db,news_detail.id)
    if not views_res:
        raise HTTPException(status_code=500,detail="更新新闻浏览量失败")
    related_news=await news.get_related_news(db,news_detail.id,news_detail.category_id)

    return {
        "code":200,
        "message":"success",
        "data":{
            "id":news_detail.id,
            "title":news_detail.title,
            "description":news_detail.description,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "category_id":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":related_news
        }
    }