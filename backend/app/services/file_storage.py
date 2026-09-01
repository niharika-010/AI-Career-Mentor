import os
from pathlib import Path
from typing import Optional
from app.core.config import settings


class FileStorageService:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir or settings.UPLOAD_DIR)

    def _get_full_path(self, relative_path: str) -> Path:
        return (self.base_dir / relative_path).resolve()

    async def save_file(self, file_bytes: bytes, subfolder: str, filename: str) -> str:
        """
        Saves file bytes to a subfolder under base_dir outside the database.
        Returns the relative path string (e.g. 'resumes/550e8400-e29b-41d4-a716-446655440000.pdf').
        """
        target_dir = self.base_dir / subfolder
        target_dir.mkdir(parents=True, exist_ok=True)
        
        relative_path = os.path.join(subfolder, filename).replace("\\", "/")
        full_path = self.base_dir / relative_path

        with open(full_path, "wb") as f:
            f.write(file_bytes)

        return relative_path

    async def delete_file(self, relative_path: str) -> bool:
        """
        Safely deletes a stored file from disk if present.
        """
        if not relative_path:
            return False
        
        full_path = self._get_full_path(relative_path)
        if full_path.exists() and full_path.is_file():
            try:
                os.remove(full_path)
                return True
            except OSError:
                return False
        return False

    async def get_file_bytes(self, relative_path: str) -> Optional[bytes]:
        """
        Reads file bytes from disk.
        """
        full_path = self._get_full_path(relative_path)
        if not full_path.exists() or not full_path.is_file():
            return None

        with open(full_path, "rb") as f:
            return f.read()


file_storage_service = FileStorageService()
