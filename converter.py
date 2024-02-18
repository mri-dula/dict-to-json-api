import ast
import json
from exceptions import InvalidDictError


def _convert_dict(dikt: ast.Dict, converted_dict={}) -> dict:
    for i, key in enumerate(dikt.keys):
        val = dikt.values[i]
        match type(val):
            case ast.Constant:
                converted_dict[key.value] = val.value
            case ast.Dict:
                converted_dict[key.value] = _convert_dict(dikt=val, converted_dict={})
            case _:
                converted_dict[key.value] = ast.unparse(val)
    return converted_dict


def convert(dikt: str, beautify=False) -> str:
    try:
        level_0 = ast.parse(dikt)
        if not isinstance(level_0, ast.Module):
            raise InvalidDictError(message="There is something wrong with the dict")
        if len(level_0.body) > 1:
            raise InvalidDictError(message="There is something wrong with the dict")
        if not isinstance(level_0.body[0], ast.Expr):
            raise InvalidDictError(message="There is something wrong with the dict")
        if not isinstance(level_0.body[0].value, ast.Dict):
            raise InvalidDictError(message="There is something wrong with the dict")
        dikt = _convert_dict(dikt=ast.parse(dikt).body[0].value)
        if beautify:
            return json.dumps(dikt, indent=2)
        return json.dumps(dikt, separators=(",", ":"))
    except SyntaxError as e:
        raise InvalidDictError(
            message="There is something wrong with the dict",
            lineno=e.lineno,
            line=e.text,
        )
