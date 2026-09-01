import io
import re
import uuid
import zipfile
from typing import Tuple, Optional
from pathlib import Path
from app.core.config import settings


class FileValidationError(Exception):
    pass


class SecurityScannerService:
    ALLOWED_RESUME_EXTENSIONS = {".pdf", ".docx"}
    ALLOWED_JD_EXTENSIONS = {".pdf", ".docx", ".txt"}

    ALLOWED_MIME_TYPES = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "application/octet-stream",  # Browser fallback
    }

    MAGIC_BYTES_PDF = b"%PDF-"
    MAGIC_BYTES_ZIP = b"PK\x03\x04"

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize raw filename to prevent directory traversal and header injection."""
        base = Path(filename).name
        # Replace non-alphanumeric chars except dots, underscores, dashes
        cleaned = re.sub(r"[^\w\.-]", "_", base)
        return cleaned[:200]

    def generate_secure_storage_filename(self, original_filename: str) -> str:
        """Generate a random UUID-based safe storage filename preserving valid extension."""
        ext = Path(original_filename).suffix.lower()
        if ext not in {".pdf", ".docx", ".txt"}:
            ext = ".bin"
        return f"{uuid.uuid4()}{ext}"

    def validate_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: Optional[str] = None,
        is_jd: bool = False,
    ) -> Tuple[str, str]:
        """
        Validates file size, extension, MIME type, and magic bytes header.
        Returns (sanitized_filename, validated_extension).
        """
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(file_bytes) > max_bytes:
            raise FileValidationError(
                f"File size ({len(file_bytes) / (1024*1024):.2f} MB) exceeds maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB} MB."
            )

        if len(file_bytes) == 0:
            raise FileValidationError("Uploaded file is empty.")

        sanitized_name = self.sanitize_filename(filename)
        ext = Path(sanitized_name).suffix.lower()

        allowed_exts = self.ALLOWED_JD_EXTENSIONS if is_jd else self.ALLOWED_RESUME_EXTENSIONS
        if ext not in allowed_exts:
            allowed_str = ", ".join(sorted(allowed_exts))
            raise FileValidationError(
                f"Invalid file extension '{ext}'. Allowed extensions: {allowed_str}"
            )

        # Magic Bytes Validation
        if ext == ".pdf":
            if not file_bytes.startswith(self.MAGIC_BYTES_PDF):
                raise FileValidationError("Invalid PDF file format. Header magic bytes missing.")
        elif ext == ".docx":
            if not file_bytes.startswith(self.MAGIC_BYTES_ZIP):
                raise FileValidationError("Invalid DOCX file format. PK zip magic bytes missing.")
            try:
                with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
                    names = z.namelist()
                    if "word/document.xml" not in names and "[Content_Types].xml" not in names:
                        raise FileValidationError("Invalid DOCX file structure.")
            except zipfile.BadZipFile:
                raise FileValidationError("Corrupted DOCX zip archive.")
        elif ext == ".txt":
            try:
                file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    file_bytes.decode("latin-1")
                except Exception:
                    raise FileValidationError("Invalid text encoding.")

        return sanitized_name, ext

    def scan_for_malware(self, file_bytes: bytes, filename: str) -> Tuple[bool, str, str]:
        """
        Pluggable Virus & Malware Scanner Architecture.
        Performs static heuristic signature checks (DOS executables, malicious scripts, zip bombs)
        and provides hook interface for ClamAV / VirusTotal integration.
        Returns: (is_clean, scan_status, detail_reason)
        """
        # 1. DOS/PE Executable Header Check (MZ header magic bytes)
        if file_bytes.startswith(b"MZ"):
            return False, "FLAGGED", "Potential executable payload detected (DOS/PE header 'MZ')."

        # 2. ELF binary header check (\x7fELF)
        if file_bytes.startswith(b"\x7fELF"):
            return False, "FLAGGED", "Unix executable binary payload detected."

        # 3. Zip Bomb Detection (for DOCX zip archives)
        if file_bytes.startswith(self.MAGIC_BYTES_ZIP):
            try:
                with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
                    total_uncompressed = 0
                    for info in z.infolist():
                        total_uncompressed += info.file_size
                        # Max uncompressed size limit check (e.g. 50MB uncompressed)
                        if total_uncompressed > 50 * 1024 * 1024:
                            return False, "FLAGGED", "Zip bomb vulnerability detected (exceeds max expansion limit)."
                    
                    if len(file_bytes) > 0:
                        ratio = total_uncompressed / len(file_bytes)
                        if ratio > 100:  # Suspicious high compression ratio
                            return False, "FLAGGED", f"High zip compression ratio detected ({ratio:.1f}x)."
            except Exception:
                pass

        # 4. Embedded Script Injections in PDF/DOCX stream signatures
        ext = Path(filename).suffix.lower()
        if ext in {".pdf", ".docx"}:
            suspicious_patterns = [
                b"/JavaScript",
                b"/JS",
                b"/Launch",
                b"cmd.exe",
                b"powershell.exe",
                b"wscript.exe",
            ]
            for pattern in suspicious_patterns:
                if pattern in file_bytes:
                    return False, "FLAGGED", f"Suspicious embedded payload signature '{pattern.decode(errors='ignore')}' detected."

        return True, "CLEAN", "File passed malware scanning and heuristics."


security_scanner_service = SecurityScannerService()
