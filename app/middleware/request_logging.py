import time
import uuid
import logging
from fastapi import Request

async def request_logging_middleware(request: Request, call_next):
    req_id = str(uuid.uuid4())[:8]
    start = time.time()

    response = await call_next(request)

    latency_ms = (time.time() - start) * 1000
    logging.info(f"[{req_id}] {request.method} {request.url.path} -> {response.status_code} ({latency_ms:.2f}ms)")

    response.headers["X-Request-Id"] = req_id
    return response
