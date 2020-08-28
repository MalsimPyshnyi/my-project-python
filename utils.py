import settings
from errors import NotFound

def normalize_path(path: str) -> str:
    if not path:
        return "/"

    normalized_path = path

    if normalized_path[-1] != "/":
        normalized_path = f"{normalized_path}/"

    return normalized_path

def to_bytes(text) -> bytes:
    if isinstance(text, bytes):
        return text

    if not isinstance(text, str):
        msg = f"cannot convert {type(text)} to bytes"
        raise ValueError(msg)

    result = text.encode()
    return result


def read_static(path: str) -> bytes:
    static = settings.STATIC_DIR / path
    if not static.is_file():
        full_path = static.resolve().as_posix()
        msg = f"file <{full_path}> not found"
        raise NotFound(msg)

    with static.open("rb") as fp:
        result = fp.read()

    return result

def get_content_type(file_path: str) -> str:
    if not file_path:
        return "text/html"
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type


def get_name_from_qs(qs: str) -> str:
    if not qs:
        return "world"

    pairs = qs.split("&")

    for pair in pairs:
        if "=" not in pair:
            continue
        key, value = pair.split("=")
        if key == "xxx":
            return value

    return "world"