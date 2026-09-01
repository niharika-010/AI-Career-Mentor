from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.rate_limit import rate_limiter
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_password_reset_token,
    decode_token,
    get_password_hash,
    verify_password,
    verify_password_reset_token,
)
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    MsgResponse,
    RefreshTokenRequest,
    ResetPasswordRequest,
    Token,
    UserLogin,
    UserOut,
    UserRegister,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register Candidate or Recruiter Account",
    dependencies=[Depends(rate_limiter(max_requests=10, window_seconds=60))],
)
async def register(
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Register a new user with duplicate email check and password hashing."""
    stmt = select(User).where(User.email == user_in.email)
    existing_user = (await db.execute(stmt)).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    access_token = create_access_token(subject=user.id, role=user.role.value)
    refresh_token = create_refresh_token(subject=user.id)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserOut.model_validate(user),
    )


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Authenticate User & Obtain JWT Tokens",
    dependencies=[Depends(rate_limiter(max_requests=15, window_seconds=60))],
)
async def login(
    user_in: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Authenticate user with email and password and return access/refresh tokens."""
    stmt = select(User).where(User.email == user_in.email)
    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive. Please contact support.",
        )

    access_token = create_access_token(subject=user.id, role=user.role.value)
    refresh_token = create_refresh_token(subject=user.id)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserOut.model_validate(user),
    )


@router.post(
    "/refresh",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token using Valid Refresh Token",
)
async def refresh_token(
    req: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Rotate access token using valid refresh token."""
    try:
        payload = decode_token(req.refresh_token)
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if not user_id or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    stmt = select(User).where(User.id == user_id)
    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    new_access_token = create_access_token(subject=user.id, role=user.role.value)
    new_refresh_token = create_refresh_token(subject=user.id)

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        user=UserOut.model_validate(user),
    )


@router.post(
    "/forgot-password",
    response_model=MsgResponse,
    status_code=status.HTTP_200_OK,
    summary="Initiate Password Recovery Flow",
    dependencies=[Depends(rate_limiter(max_requests=5, window_seconds=60))],
)
async def forgot_password(
    req: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
) -> MsgResponse:
    """Send password reset instructions if user exists."""
    stmt = select(User).where(User.email == req.email)
    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user:
        # Prevent email enumeration by returning generic message
        return MsgResponse(
            message="If an account with that email exists, password reset instructions have been sent."
        )

    reset_token = create_password_reset_token(email=user.email)
    
    return MsgResponse(
        message="If an account with that email exists, password reset instructions have been sent.",
        reset_token=reset_token,
    )


@router.post(
    "/reset-password",
    response_model=MsgResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset User Password with Reset Token",
)
async def reset_password(
    req: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
) -> MsgResponse:
    """Reset user password using password reset token."""
    email = verify_password_reset_token(req.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token.",
        )

    stmt = select(User).where(User.email == email)
    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    user.hashed_password = get_password_hash(req.new_password)
    await db.commit()

    return MsgResponse(message="Password has been reset successfully.")


@router.get(
    "/me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Fetch Current Authenticated User Profile",
)
async def read_current_user(
    current_user: User = Depends(get_current_active_user),
) -> UserOut:
    """Retrieve authenticated user details."""
    return UserOut.model_validate(current_user)
