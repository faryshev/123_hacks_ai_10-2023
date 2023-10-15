"""
Модуль API ping.
"""
from fastapi import APIRouter


router = APIRouter()


@router.get("")
async def ping():
    """
    API PING-PONG.
    """
    return 'PONG'
