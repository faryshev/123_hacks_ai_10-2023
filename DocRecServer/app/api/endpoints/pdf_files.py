"""
Модуль API exchange.
"""
import typing
import sqlalchemy as sa
from fastapi import Depends, APIRouter, UploadFile, File
from fastapi.responses import FileResponse

from app import schemas, models, db

from pathlib import Path


router = APIRouter()

# TODO remove this make with globals server param
pdf_directory = Path("pdfs")
pdf_directory.mkdir(exist_ok=True)


@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile):
    if file.filename.endswith(".pdf"):
        with open(pdf_directory / file.filename, "wb") as pdf_file:
            pdf_file.write(file.file.read())
        return {"message": "Файл успешно загружен"}
    else:
        return {"error": "Файл не является PDF-документом"}


@router.get("/download_pdf/{file_name}")
async def download_pdf(file_name: str):
    pdf_path = pdf_directory / file_name
    if pdf_path.is_file():
        response = FileResponse(pdf_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})
        return response
    else:
        return {"error": "Файл не найден"}
    
@router.get("/download_stats/{file_name}")
async def download_pdf(file_name: str):
    pdf_path = pdf_directory / file_name
    if pdf_path.is_file():
        response = FileResponse(pdf_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})
        return response
    else:
        return {"error": "Файл не найден"}
    
@router.get("/download_output/{file_name}")
async def download_pdf(file_name: str):
    pdf_path = pdf_directory / file_name
    if pdf_path.is_file():
        response = FileResponse(pdf_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})
        return response
    else:
        return {"error": "Файл не найден"}
