import json
import uuid
from typing import Any


def make_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def json_bytes(payload: Any) -> bytes:
    return json.dumps(payload).encode("utf-8")


def read_json(body: bytes) -> dict[str, Any]:
    if not body:
        return {}

    return json.loads(body.decode("utf-8"))
