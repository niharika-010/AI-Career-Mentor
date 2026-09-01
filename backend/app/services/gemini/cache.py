import hashlib
import threading
from typing import Any, Optional


class AIResponseCache:
    """Thread-safe in-memory cache for structured AI responses to prevent duplicate LLM calls and avoid rate limits."""

    def __init__(self, max_size: int = 250):
        self.max_size = max_size
        self._cache = {}
        self._lock = threading.Lock()

    def _compute_key(self, task_name: str, payload_str: str) -> str:
        raw = f"{task_name}:{payload_str}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def get(self, task_name: str, payload_str: str) -> Optional[Any]:
        key = self._compute_key(task_name, payload_str)
        with self._lock:
            return self._cache.get(key)

    def set(self, task_name: str, payload_str: str, value: Any) -> None:
        key = self._compute_key(task_name, payload_str)
        with self._lock:
            if len(self._cache) >= self.max_size:
                # Evict oldest entry
                first_key = next(iter(self._cache))
                del self._cache[first_key]
            self._cache[key] = value

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()


ai_response_cache = AIResponseCache()
