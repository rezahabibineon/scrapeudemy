from typing import Optional
from fastapi import APIRouter, Query
from apps.controller import NewsController

router = APIRouter()

@router.get("/get_news")
async def get_news(num_news : Optional[int]=Query(None, example=1)):
    total, data =  NewsController.get_news(num_news)
    return {
        "total": total,
        "data": data,
    }