# services/file_service.py
import uuid
from fastapi import UploadFile, HTTPException, status
from pathlib import Path


class FileService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.create_upload_dir()

    def create_upload_dir(self):
        """Создает директорию для загрузок если она не существует"""
        self.upload_dir.mkdir(exist_ok=True)

    async def save_upload_file(self, upload_file: UploadFile) -> dict:
        """Сохраняет загруженный файл и возвращает информацию о нем"""
        try:
            # Генерируем уникальное имя файла
            file_extension = (
                Path(upload_file.filename).suffix if upload_file.filename else ""
            )
            unique_filename = f"{uuid.uuid4()}{file_extension}"

            # Сохраняем файл
            file_path = self.upload_dir / unique_filename

            # Читаем и сохраняем файл
            content = await upload_file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            # Возвращаем информацию о файле
            return {
                "filename": upload_file.filename,
                "server_path": str(file_path),
                "file_size": len(content),
                "content_type": upload_file.content_type,
                "saved_filename": unique_filename,
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при сохранении файла: {str(e)}",
            )

    def delete_file(self, server_path: str) -> bool:
        """Удаляет файл с сервера"""
        try:
            file_path = Path(server_path)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False


# Создаем экземпляр сервиса
file_service = FileService()
