from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.job import JobDescription
from app.schemas.job import JobDescriptionCreate, JobDescriptionOut, JobDescriptionListOut
from app.services.security_scanner import security_scanner_service, FileValidationError
from app.services.file_storage import file_storage_service
from app.services.document_parser import parse_pdf, parse_docx, parse_txt, normalize_document, DocumentParsingError

router = APIRouter()


@router.post(
    "",
    response_model=JobDescriptionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create or upload a job description (JSON text or file)",
)
async def create_job_description(
    title: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    raw_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> JobDescriptionOut:
    """
    Create a job description via raw text or file upload (PDF/DOCX/TXT).
    Normalizes requirements and stores metadata.
    """
    final_title = title.strip() if title else ""
    final_company = company_name.strip() if company_name else None
    final_text = raw_text.strip() if raw_text else ""
    
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    scan_status: str = "CLEAN"

    if file and file.filename:
        file_bytes = await file.read()
        
        # 1. File Validation
        try:
            sanitized_filename, ext = security_scanner_service.validate_file(
                file_bytes=file_bytes,
                filename=file.filename,
                content_type=file.content_type,
                is_jd=True,
            )
        except FileValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        # 2. Security / Malware Scan
        is_clean, scan_status, scan_reason = security_scanner_service.scan_for_malware(
            file_bytes=file_bytes,
            filename=sanitized_filename,
        )
        if not is_clean:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Security scan rejected JD file: {scan_reason}",
            )

        # 3. Document Parsing
        try:
            if ext == ".pdf":
                extracted_text = parse_pdf(file_bytes)
            elif ext == ".docx":
                extracted_text = parse_docx(file_bytes)
            elif ext == ".txt":
                extracted_text = parse_txt(file_bytes)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format.")
        except DocumentParsingError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

        # Combine text or set extracted text
        final_text = extracted_text if not final_text else f"{final_text}\n\n{extracted_text}"
        
        if not final_title:
            # Fallback title if not supplied in form
            final_title = sanitized_filename.rsplit(".", 1)[0].replace("_", " ").title()

        # 4. Save file outside DB
        storage_filename = security_scanner_service.generate_secure_storage_filename(sanitized_filename)
        relative_path = await file_storage_service.save_file(
            file_bytes=file_bytes,
            subfolder="job_descriptions",
            filename=storage_filename,
        )

        file_name = sanitized_filename
        file_path = relative_path
        file_type = file.content_type or f"application/{ext.replace('.', '')}"
        file_size_bytes = len(file_bytes)

    if not final_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job title is required.",
        )

    if not final_text or len(final_text) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description text or valid document file must be provided (at least 10 characters).",
        )

    # Normalize Document Requirements
    parsed_requirements = normalize_document(final_text, doc_type="job_description")

    job_desc = JobDescription(
        user_id=current_user.id,
        title=final_title,
        company_name=final_company,
        raw_text=final_text,
        parsed_requirements=parsed_requirements,
        file_name=file_name,
        file_path=file_path,
        file_type=file_type,
        file_size_bytes=file_size_bytes,
        scan_status=scan_status,
    )

    db.add(job_desc)
    await db.commit()
    await db.refresh(job_desc)

    return JobDescriptionOut.model_validate(job_desc)


@router.post(
    "/text",
    response_model=JobDescriptionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create job description via JSON body",
)
async def create_job_description_json(
    body: JobDescriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> JobDescriptionOut:
    """Create a job description directly via JSON body."""
    parsed_requirements = normalize_document(body.raw_text, doc_type="job_description")

    job_desc = JobDescription(
        user_id=current_user.id,
        title=body.title.strip(),
        company_name=body.company_name.strip() if body.company_name else None,
        raw_text=body.raw_text.strip(),
        parsed_requirements=parsed_requirements,
        scan_status="CLEAN",
    )

    db.add(job_desc)
    await db.commit()
    await db.refresh(job_desc)

    return JobDescriptionOut.model_validate(job_desc)


@router.get(
    "",
    response_model=JobDescriptionListOut,
    status_code=status.HTTP_200_OK,
    summary="List authenticated user's job descriptions",
)
async def list_job_descriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> JobDescriptionListOut:
    """Retrieve paginated list of job descriptions for current user."""
    stmt = (
        select(JobDescription)
        .where(JobDescription.user_id == current_user.id)
        .order_by(JobDescription.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    results = (await db.execute(stmt)).scalars().all()

    count_stmt = select(func.count(JobDescription.id)).where(JobDescription.user_id == current_user.id)
    total = (await db.execute(count_stmt)).scalar() or 0

    items = [JobDescriptionOut.model_validate(j) for j in results]
    return JobDescriptionListOut(items=items, total=total)


@router.get(
    "/{job_id}",
    response_model=JobDescriptionOut,
    status_code=status.HTTP_200_OK,
    summary="Fetch single job description details & parsed requirements",
)
async def get_job_description(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> JobDescriptionOut:
    """Get job description by ID for current user."""
    stmt = select(JobDescription).where(JobDescription.id == job_id, JobDescription.user_id == current_user.id)
    job_desc = (await db.execute(stmt)).scalar_one_or_none()

    if not job_desc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found.",
        )

    return JobDescriptionOut.model_validate(job_desc)


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete job description and stored file",
)
async def delete_job_description(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete job description record from DB and remove file if present."""
    stmt = select(JobDescription).where(JobDescription.id == job_id, JobDescription.user_id == current_user.id)
    job_desc = (await db.execute(stmt)).scalar_one_or_none()

    if not job_desc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found.",
        )

    if job_desc.file_path:
        await file_storage_service.delete_file(job_desc.file_path)

    await db.delete(job_desc)
    await db.commit()

    return {"message": "Job description deleted successfully", "id": job_id}
