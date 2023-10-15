"""
Основной модуль сервера.
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

import uvicorn
from pytz import timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import db
from app.api.endpoints import api_router
from app.core.config import base_config


log_config = uvicorn.config.LOGGING_CONFIG
FORMAT_LOGS = '%(levelname)-10s | %(asctime)-15s - %(message)s'

log_config["formatters"]["access"]["fmt"] = FORMAT_LOGS
log_config["formatters"]["default"]["fmt"] = FORMAT_LOGS

if base_config.LOGGER:
    os.makedirs(base_config.LOGS_PATH, exist_ok=True)

    logger_access = logging.getLogger("uvicorn.access")
    logger_error = logging.getLogger("uvicorn.error")

    handler = TimedRotatingFileHandler(
        filename=os.path.join(base_config.LOGS_PATH, 'server.log'),
        when='midnight',
        backupCount=base_config.LOGS_COUNT
    )
    handler.setFormatter(logging.Formatter(FORMAT_LOGS))

    logger_access.addHandler(handler)
    logger_error.addHandler(handler)


app = FastAPI(
    title=base_config.PROJECT_NAME,
    version=base_config.PROJECT_VERSION,
    openapi_url='/openapi.json' if base_config.OPENAPI else None
)

app.include_router(api_router)


# scheduler = AsyncIOScheduler(timezone=timezone('Europe/Moscow'))


@app.on_event("startup")
async def startup_event():
    await db.init_db()


if base_config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=base_config.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host=base_config.SERVER_HOST,
        port=base_config.SERVER_PORT,
        workers=base_config.WORKERS,
        log_config=log_config
    )
