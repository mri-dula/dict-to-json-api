import ast
import json
from exceptions import InvalidDictError
import re


def _clean_dict_string(dikt: str) -> str:
    object_representation_matches = re.findall(
        ":\s*<[a-zA-Z\.0-9]+\sobject\sat\s[0-9a-zA-Z]+>", dikt
    )
    cleaned_dikt = f"{dikt}"
    for match in object_representation_matches:
        object_representation = match.split(":", 1)[1].strip()
        cleaned_dikt = cleaned_dikt.replace(
            match, f":{json.dumps(object_representation)}"
        )
    return cleaned_dikt


def _convert_dict(dikt: ast.Dict, converted_dict=None) -> dict:
    if converted_dict is None:
        converted_dict = {}
    for i, key in enumerate(dikt.keys):
        val = dikt.values[i]
        if isinstance(val, ast.Constant):
            converted_dict[key.value] = val.value
        elif isinstance(val, ast.Dict):
            converted_dict[key.value] = _convert_dict(dikt=val, converted_dict={})
        else:
            converted_dict[key.value] = ast.unparse(val)
    return converted_dict


def convert(dikt: str, beautify=False) -> str:
    try:
        dikt = _clean_dict_string(dikt)
        level_0 = ast.parse(dikt)

        if not isinstance(level_0, ast.Module):
            raise InvalidDictError(message="There is something wrong with the dict")
        if len(level_0.body) > 1:
            raise InvalidDictError(message="There is something wrong with the dict")
        if not isinstance(level_0.body[0], ast.Expr):
            raise InvalidDictError(message="There is something wrong with the dict")
        if not isinstance(level_0.body[0].value, ast.Dict):
            raise InvalidDictError(message="There is something wrong with the dict")
        dikt = _convert_dict(dikt=level_0.body[0].value)
        if beautify:
            return json.dumps(dikt, indent=2)
        return json.dumps(dikt, separators=(",", ":"))
    except SyntaxError as e:
        raise InvalidDictError(
            message="There is something wrong with the dict",
            lineno=e.lineno,
            line=e.text,
            offset=e.offset,
        )
