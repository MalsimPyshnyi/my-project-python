import mimetypes
import settings
from errors import NotFound
from custom_types import User
from urllib.parse import parse_qs


#def normalize_path(path: str) -> str:
    #if not path:
        #return "/"

    #normalized_path = path

    #if normalized_path[-1] != "/":
        #normalized_path = f"{normalized_path}/"

    #return normalized_path

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

# def get_user_data(qs: str) -> dict:
#     qp = parse_qs(qs) #Делает штуки со сплитами, запомнить!
#     name = qp.get("name", ["world"])[0] #На выходных выучить работу с диктами
#     age = int(qp.get("name", [0])[0])
#
#     return User(name=name, age=age)

def get_user_data(qs: str) -> User:
    qp = parse_qs(qs)

    default_list_of_names = "world"
    default_list_of_ages = "0"

    list_of_names = qp.get("name", default_list_of_names)
    list_of_ages = qp.get("age", default_list_of_ages)

    name = list_of_names[0]
    age = int(list_of_ages[0])

    return User(name=name, age=age)

#def get_name_from_qs(qs: str) -> str:
    #name = "world"

    #if qs:
        #pairs = qs.split("&")

    #for pair in pairs:
        #if "=" not in pair:
            #continue
        #key, value = pair.split("=")
        #if key == "xxx":
            #name = value
            #break

    #return name

# def get_age_from_qs(qs: str) ->int:
#     if not qs:
#         return 2020
#
#     pairs = qs.split("&")
#
#     for pair in pairs:
#         if "=" not in pair:
#             continue
#         key, value = pair.split("=")
#         if key == "yyy":
#             return value
#
#         return 2020