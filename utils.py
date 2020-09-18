import json
import os
from http import cookies
from pathlib import Path
from typing import AnyStr
from typing import Dict
from typing import Optional

import settings
from consts import DEFAULT_THEME
from consts import SESSION_AGE
from consts import SESSION_COOKIE
from consts import THEMES
from errors import NotFound


def to_bytes(text: AnyStr) -> bytes:

    if isinstance(text, bytes):
        return text

    if not isinstance(text, str):
        err_msg = f"cannot convert {type(text)} to bytes"
        raise ValueError(err_msg)

    result = text.encode()
    return result


def to_str(text: AnyStr) -> str:

    result = text

    if not isinstance(text, (str, bytes)):
        result = str(text)

    if isinstance(result, bytes):
        result = result.decode()

    return result


def read_static(path: str) -> bytes:

    static_obj = settings.STATIC_DIR / path
    if not static_obj.is_file():
        static_path = static_obj.resolve().as_posix()
        err_msg = f"file <{static_path}> not found"
        raise NotFound(err_msg)

    with static_obj.open("rb") as src:
        content = src.read()

    return content


def get_session_from_headers(headers: Optional[Dict]) -> Optional[str]:

    if not headers:
        return None

    cookie_header = headers.get("Cookie")
    if not cookie_header:
        return None

    jar = cookies.SimpleCookie()
    jar.load(cookie_header)
    if SESSION_COOKIE not in jar:
        return None

    session_morsel = jar[SESSION_COOKIE]
    return session_morsel.value


def generate_new_session() -> str:

    session = os.urandom(16).hex()
    return session


def build_session_header(session: str, expires: bool = False) -> str:

    jar = cookies.SimpleCookie()
    jar[SESSION_COOKIE] = session
    morsel = jar[SESSION_COOKIE]

    morsel["Domain"] = settings.SITE
    morsel["Path"] = "/"

    max_ages = {
        False: SESSION_AGE,
        True: 0,
    }
    morsel["Max-Age"] = max_ages[expires]

    header = jar[SESSION_COOKIE].OutputString()

    return header


def switch_theme(current_theme: Optional[str]) -> str:

    themes = sorted(THEMES)
    themes_fsm = {th1: th2 for th1, th2 in zip(themes, reversed(themes))}

    new_theme = themes_fsm[current_theme or DEFAULT_THEME]

    return new_theme


def load_theme(session: Optional[str]) -> str:

    data = load_session_data(session)

    return data.get("theme", DEFAULT_THEME)


def store_theme(session: Optional[str], theme: Optional[str]) -> None:

    if not session:
        return

    session_data = load_session_data(session)

    session_data["theme"] = theme or DEFAULT_THEME

    store_session_data(session, session_data)


def load_profile(session: Optional[str]) -> Optional[str]:

    data = load_session_data(session)

    return data.get("profile")


def store_profile(session: Optional[str], profile: str) -> None:

    if not session:
        return

    session_data = load_session_data(session)

    session_data["profile"] = profile

    store_session_data(session, session_data)


def drop_profile(session: Optional[str]) -> None:

    if not session:
        return

    session_data = load_session_data(session)
    session_data["profile"] = None
    store_session_data(session, session_data)


def load_session_data(session: Optional[str]) -> Dict:


    empty_dict = {}

    if not session:
        return empty_dict

    data_file = get_data_file(session)
    if not data_file.is_file():
        return empty_dict

    with data_file.open("r") as src:
        data = json.load(src)

    return data or empty_dict


def store_session_data(
    session: Optional[str], new_session_data: Optional[Dict]
) -> None:


    if not session:
        return

    session_data = load_session_data(session)
    session_data.update(new_session_data or {})

    data_file = get_data_file(session)
    with data_file.open("w") as dst:
        json.dump(session_data, dst)


def get_data_file(session: Optional[str]) -> Path:

    data_file = (settings.STORAGE_DIR / f"user_{session}.json").resolve()
    return data_file


    # ok = all([value, value.isdecimal(), int(value)])
    # return ok

# import mimetypes
# from typing import AnyStr
# from urllib.parse import parse_qs
#
# import settings
# from custom_types import User
# from errors import NotFound
#
#
# #def normalize_path(path: str) -> str:
#     #if not path:
#         #return "/"
#
#     #normalized_path = path
#
#     #if normalized_path[-1] != "/":
#         #normalized_path = f"{normalized_path}/"
#
#     #return normalized_path
#
# def to_bytes(text: AnyStr) -> bytes:
#     if isinstance(text, bytes):
#         return text
#
#     if not isinstance(text, str):
#         msg = f"cannot convert {type(text)} to bytes"
#         raise ValueError(msg)
#
#     result = text.encode()
#     return result
#
#
# def read_static(path: str) -> bytes:
#     static_obj = settings.STATIC_DIR / path
#     if not static_obj.is_file():
#         static_path = static_obj.resolve().as_posix()
#         err_msg = f"file <{static_path}> not found"
#         raise NotFound(err_msg)
#
#     with static_obj.open("rb") as src:
#         result = src.read()
#
#     return result
#
# def get_content_type(file_path: str) -> str:
#     if not file_path:
#         return "text/html"
#     content_type, _ = mimetypes.guess_type(file_path)
#     return content_type
#
# # def get_user_data(qs: str) -> dict:
# #     qp = parse_qs(qs) #Делает штуки со сплитами, запомнить!
# #     name = qp.get("name", ["world"])[0] #На выходных выучить работу с диктами
# #     age = int(qp.get("name", [0])[0])
# #
# #     return User(name=name, age=age)
#
# def get_user_data(query: str) -> User:
#
#     anonymous = User.default()
#
#     try:
#         key_value_pairs = parse_qs(query, strict_parsing=True)
#     except ValueError:
#         return anonymous
#
#     name_values = key_value_pairs.get("name", [anonymous.name])
#     name = name_values[0]
#
#     age_values = key_value_pairs.get("age", [anonymous.age])
#     age = age_values[0]
#     if isinstance(age, str) and age.isdecimal():
#         age = int(age)
#
#     return User(name=name, age=age)
#
# #def get_name_from_qs(qs: str) -> str:
#     #name = "world"
#
#     #if qs:
#         #pairs = qs.split("&")
#
#     #for pair in pairs:
#         #if "=" not in pair:
#             #continue
#         #key, value = pair.split("=")
#         #if key == "xxx":
#             #name = value
#             #break
#
#     #return name
#
# # def get_age_from_qs(qs: str) ->int:
# #     if not qs:
# #         return 2020
# #
# #     pairs = qs.split("&")
# #
# #     for pair in pairs:
# #         if "=" not in pair:
# #             continue
# #         key, value = pair.split("=")
# #         if key == "yyy":
# #             return value
# #
# #         return 2020