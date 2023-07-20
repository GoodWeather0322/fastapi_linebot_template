from fastapi import APIRouter
from api.v1.endpoints.bot import bot

api_router = APIRouter()
api_router.include_router(bot.router, tags=["bot"], prefix='/v1/bot')