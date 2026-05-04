from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from schemas.base import NewsItemBase


class FavoriteCheckRequest(BaseModel):
    is_favorite:bool=Field(...,alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    news_id:int=Field(...,alias="newsId")

#两个类：新闻模型类+收藏模型类
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id:int=Field(alias="favoriteId")
    favorite_time:datetime=Field(...,alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,#alias/字段名兼容
        from_attributes=True# 允许从ORM对象属性中获取值
    )

#收藏列表接口响应模型类
class FavoriteListResponse(BaseModel):
    list:list[FavoriteNewsItemResponse]
    total:int
    has_more:bool=Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,#alias/字段名兼容
        from_attributes=True# 允许从ORM对象属性中获取值
    )