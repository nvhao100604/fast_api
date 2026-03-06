import os
import shutil
from uuid import uuid4
from datetime import datetime
from fastapi import UploadFile

def generate_unique_filename(user_id: int, original_filename: str) -> str:
    """Tạo tên file duy nhất: user_{id}_{timestamp}_{uuid}.ext"""
    file_ext = original_filename.split(".")[-1].lower()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid4().hex[:8]
    return f"user_{user_id}_{timestamp}_{unique_id}.{file_ext}"

def save_file_to_disk(file: UploadFile, folder_path: str, filename: str) -> str:
    """Lưu file vật lý và trả về đường dẫn đầy đủ."""
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return file_path

def check_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Kiểm tra định dạng file có hợp lệ không."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions