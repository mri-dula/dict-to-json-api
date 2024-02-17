import ast
import json
from exceptions import InvalidDictError


def convert(dikt: str, beautify=False) -> str:
    try:
        dikt = ast.literal_eval(dikt)
        if beautify:
            return json.dumps(dikt, indent=2)
        return json.dumps(dikt, separators=(",", ":"))
    except InvalidDictError:
        raise InvalidDictError("There is something wrong with the dict")
