from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.resume import Resume
from app.schemas.resume import ResumeOut, ResumeListOut
from app.services.security_scanner import security_scanner_service, FileValidationError
from app.services.file_storage import file_storage_service
from app.services.document_parser import parse_pdf, parse_docx, normalize_document, DocumentParsingError

router = APIRouter()


@router.post(
    "",
    response_model=ResumeOut,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and parse candidate resume (PDF/DOCX)",
)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ResumeOut:
    """Upload a PDF or DOCX resume, perform security checks, save file outside DB, parse, and store metadata."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided in upload request.",
        )

    file_bytes = await file.read()

    # 1. Validate File Size, Extension, and Magic Bytes
    try:
        sanitized_filename, ext = security_scanner_service.validate_file(
            file_bytes=file_bytes,
            filename=file.filename,
            content_type=file.content_type,
            is_jd=False,
        )
    except FileValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # 2. Virus & Malware Scanning
    is_clean, scan_status, scan_reason = security_scanner_service.scan_for_malware(
        file_bytes=file_bytes,
        filename=sanitized_filename,
    )
    if not is_clean:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Security scan rejected file: {scan_reason}",
        )

    # 3. Document Parsing
    try:
        if ext == ".pdf":
            raw_text = parse_pdf(file_bytes)
        elif ext == ".docx":
            raw_text = parse_docx(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="Unsupported resume format.")
    except DocumentParsingError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    # 4. Document Normalization (Preprocessed structure)
    parsed_data = normalize_document(raw_text, doc_type="resume")

    # 5. Save File Outside Database
    storage_filename = security_scanner_service.generate_secure_storage_filename(sanitized_filename)
    relative_path = await file_storage_service.save_file(
        file_bytes=file_bytes,
        subfolder="resumes",
        filename=storage_filename,
    )

    # 6. Store Metadata & Parsed JSON in DB
    resume = Resume(
        user_id=current_user.id,
        file_name=sanitized_filename,
        file_path=relative_path,
        file_type=file.content_type or f"application/{ext.replace('.', '')}",
        file_size_bytes=len(file_bytes),
        parsed_data=parsed_data,
        scan_status=scan_status,
    )

    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    return ResumeOut.model_validate(resume)


@router.get(
    "",
    response_model=ResumeListOut,
    status_code=status.HTTP_200_OK,
    summary="List authenticated user's uploaded resumes",
)
async def list_resumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ResumeListOut:
    """Retrieve paginated list of resumes for current user."""
    stmt = (
        select(Resume)
        .where(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    results = (await db.execute(stmt)).scalars().all()

    count_stmt = select(func.count(Resume.id)).where(Resume.user_id == current_user.id)
    total = (await db.execute(count_stmt)).scalar() or 0

    items = [ResumeOut.model_validate(r) for r in results]
    return ResumeListOut(items=items, total=total)


@router.get(
    "/{resume_id}",
    response_model=ResumeOut,
    status_code=status.HTTP_200_OK,
    summary="Fetch single resume details & parsed data",
)
async def get_resume(
    resume_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ResumeOut:
    """Get resume by ID for current user."""
    stmt = select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    resume = (await db.execute(stmt)).scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    return ResumeOut.model_validate(resume)


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete resume and stored file",
)
async def delete_resume(
    resume_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete resume record from DB and remove file from disk."""
    stmt = select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    resume = (await db.execute(stmt)).scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    # Delete file from disk
    await file_storage_service.delete_file(resume.file_path)

    # Delete from DB
    await db.delete(resume)
    await db.commit()

    return {"message": "Resume deleted successfully", "id": resume_id}
