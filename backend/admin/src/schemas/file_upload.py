# schemas/file_upload.py
from pydantic import BaseModel
from uuid import UUID


class FileUploadResponse(BaseModel):
    filename: str
    server_path: str
    file_size: int
    content_type: str


class ContentCreateWithUpload(BaseModel):
    menu_id: UUID
    type: int
    file: str  # Это будет временный путь после загрузки
