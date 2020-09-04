from custom_types import HttpRequest
from custom_types import User
from settings import STORAGE_DIR

ANONYMOUS_USER = User(name="anonymous", age=0)
ROOT_REQUEST = HttpRequest(method="get", original="", normal="/")
USERS_DATA = STORAGE_DIR / "users.txt"