import time
from collections import defaultdict
from typing import Dict, List
from fastapi import HTTPException, Request, status

from app.core.config import settings

# In-memory sliding window rate limiter
# ip_address -> list of timestamps
_request_history: Dict[str, List[float]] = defaultdict(list)


def rate_limiter(max_requests: int = 10, window_seconds: int = 60):
    """FastAPI dependency enforcing sliding window rate limiting per IP address."""
    async def _rate_limit_dependency(request: Request):
        # Bypass rate limiter during testing environment
        if settings.ENVIRONMENT.lower() in ["testing", "test"]:
            return

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        
        # Clean timestamps older than window_seconds
        cutoff = now - window_seconds
        _request_history[client_ip] = [t for t in _request_history[client_ip] if t > cutoff]

        if len(_request_history[client_ip]) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds.",
            )

        _request_history[client_ip].append(now)

    return _rate_limit_dependency
