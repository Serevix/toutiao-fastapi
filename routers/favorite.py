from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteCheckRequest, FavoriteAddRequest, FavoriteListResponse, FavoriteNewsItemResponse
from utils.auth import get_current_user
from utils.response import success_response

router=APIRouter(prefix="/api/favorite",tags=["favorite"])

@router.get("/check")
async def check_favorite(
        news_id:int=Query(...,alias="newsId"),
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    is_favorite=await favorite.is_news_favorite(db,user.id,news_id)
    return success_response(msg="检查成功",data=FavoriteCheckRequest(isFavorite=is_favorite))


@router.post("/add")
async def add_favorite(
        data:FavoriteAddRequest,#使用 Pydantic 模型接收 因为
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    result=await favorite.add_favorite(db,user.id,data.news_id)
    return success_response(msg="收藏成功favorite",data=result)

@router.delete("/remove")
async def remove_favorite(
        news_id:int=Query(...,alias="newsId"), #使用 Query 参数接收
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    result=await favorite.delete_favorite(db,user.id,news_id)
    if not result:
        raise HTTPException(status_code=404,detail="收藏不存在")
    return success_response(msg="取消收藏成功")

@router.get("/list")
async def get_favorite_list(
        page:int=Query(1,ge=1),
        page_size:int=Query(10,alias="pageSize",le=100),
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    total,rows=await favorite.get_favorites(db,user.id,page,page_size)
    favorite_list=[
        FavoriteNewsItemResponse(
        **news.__dict__,
        favoriteTime=favorite_time,
        favoriteId=favorite_id
    ) for news,favorite_time,favorite_id in rows]
    has_more=total>page*page_size
    data=FavoriteListResponse(list=favorite_list,total=total,hasMore=has_more)
    return success_response(msg="获取收藏列表成功",data=data)

@router.get("/clear")
async def clear_favorite(
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    count=await favorite.delete_all_favorite(db,user.id)
    return success_response(msg=f"已清空{count}条收藏")