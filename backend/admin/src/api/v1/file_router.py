# routers/file_router.py
from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from uuid import UUID
from services.menu_service import MenuService, get_menu_service
from services.file_service import file_service
from schemas.entity import Message, ContentCreate

router = APIRouter()

@router.post(
    "/{menu_id}/content/upload",
    summary="Добавить контент с загрузкой файла",
    response_model=Message
)
async def add_menu_content_with_upload(
        menu_id: UUID,
        file_type: int = Form(..., description="Тип контента (1-изображение, 2-видео, 3-документ)"),
        file: UploadFile = File(..., description="Файл для загрузки"),
        menu_service: MenuService = Depends(get_menu_service),
):
    """Добавляет контент с загрузкой файла на сервер"""

    # Проверяем допустимые типы файлов
    allowed_image_types = ["image/jpeg", "image/png", "image/gif"]
    allowed_video_types = ["video/mp4", "video/avi", "video/mkv"]
    allowed_document_types = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

    if file_type == 1 and file.content_type not in allowed_image_types:
        raise HTTPException(
            status_code=400,
            detail="Недопустимый тип изображения. Разрешены: JPEG, PNG, GIF"
        )
    elif file_type == 2 and file.content_type not in allowed_video_types:
        raise HTTPException(
            status_code=400,
            detail="Недопустимый тип видео. Разрешены: MP4, AVI, MKV"
        )
    elif file_type == 3 and file.content_type not in allowed_document_types:
        raise HTTPException(
            status_code=400,
            detail="Недопустимый тип документа. Разрешены: PDF, DOC, DOCX"
        )

    content_data = ContentCreate(menu_id=menu_id,type=file_type, server_path="")  # server_path будет заполнен автоматически
    return await menu_service.add_menu_content_with_file(menu_id, content_data, file)

@router.put(
    "/{menu_id}/content/upload/{content_id}",
    summary="Обновить контент с загрузкой нового файла",
    response_model=Message
)
async def update_menu_content_with_upload(
        menu_id: UUID,
        content_id: UUID,
        file_type: int = Form(..., description="Тип контента (1-изображение, 2-видео, 3-документ)"),
        file: UploadFile = File(..., description="Новый файл для загрузки"),
        menu_service: MenuService = Depends(get_menu_service),
):
    """Обновляет контент с загрузкой нового файла на сервер"""
    content_data = ContentCreate(menu_id=menu_id,type=file_type, server_path="")
    return await menu_service.update_menu_content_with_file(content_id, content_data, file)

@router.post("/upload-test", summary="Тест загрузки файла")
async def upload_test_file(file: UploadFile = File(...)):
    """Тестовый эндпоинт для загрузки файлов"""
    file_info = await file_service.save_upload_file(file)
    return {
        "message": "Файл успешно загружен",
        "filename": file_info["filename"],
        "saved_as": file_info["saved_filename"],
        "file_size": file_info["file_size"],
        "content_type": file_info["content_type"]
    }