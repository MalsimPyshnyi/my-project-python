from typing import AnyStr

import settings
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
    """
    Safely converts any string to str.
    :param text: any string
    :return: str
    """

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