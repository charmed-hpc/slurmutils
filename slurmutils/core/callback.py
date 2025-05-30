# Copyright 2024-2025 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Callbacks for parsing and marshalling Slurm configuration models."""

__all__ = [
    "Callback",
    "DefaultCallback",
    "MultilineCallback",
    "BoolCallback",
    "StrBoolCallback",
    "IntBoolCallback",
    "QuoteCallback",
    "CommaDictCallback",
    "CommaDictColonPairCallback",
    "CommaDictColonArrayCallback",
    "SemicolonDictCallback",
    "CommaSepCallback",
    "ColonSepCallback",
    "make_callback",
]

import ast
from collections.abc import Callable, Iterable, Mapping
from functools import partial
from typing import Any, NamedTuple


class Callback(NamedTuple):
    """Callbacks for parsing and marshalling Slurm data model values.

    Args:
        parser: Callback that parses the value as read in from Slurm configuration.
        marshaller: Callback that marshals the value back into a valid Slurm configuration value.
    """

    parser: Callable[[str, str], Any]
    marshaller: Callable[[str, Any, str], str]


def make_callback(parser: Callable[[str], Any], marshaller: Callable[[Any], str]) -> Callback:
    """Make a new callback.

    Args:
        parser: Parser to initialize callback with.
        marshaller: Marshaller to initialize callback with.
    """
    return Callback(partial(_parse_base, parser), partial(_marshal_base, marshaller))


def _parse_base(parser: Callable[[str], Any], /, expr: str, sep: str) -> Any:
    """Base parser for defining Slurm configuration data parsers.

    Args:
        parser: Parser to handle value parsing and type casting.
        expr: Slurm configuration expression to parse.
        sep: Key, value separator used in Slurm configuration expression.
    """  # noqa D401
    _, v = expr.split(sep, maxsplit=1)
    return parser(v)


def _marshal_base(marshaller: Callable[[Any], str], /, key: str, value: Any, sep: str) -> str:
    """Base marshaller for defining Slurm configuration data marshallers.

    Args:
        marshaller: Marshaller to handle value marshalling and serialization.
        key: Configuration key to marshal.
        value: Configuration value to marshal.
        sep: Separator used to separate key and value in Slurm configuration.
    """  # noqa D401
    v = marshaller(value)
    # Split on newlines for non-unique configuration fields that can
    # appear more than once in a configuration file.
    return "\n".join(f"{key}{sep}{v_}" for v_ in v.strip().splitlines())


def _autocast(value: str) -> Any:
    """Autocast parsed configuration value to the 'best-fitting' Python type.

    Args:
        value: Parsed configuration value to automatically cast to the best-fitting Python type.
    """
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value


def _bool_parse(value: str) -> bool:
    match value.lower():
        case "true":
            return True
        case "false":
            return False
        case _:
            raise ValueError(f"expected true or false, not {value}")


def _bool_marshal(value: bool) -> str:
    return "true" if value else "false"


def _strbool_parse(value: str) -> bool:
    match value.lower():
        case "yes":
            return True
        case "no":
            return False
        case _:
            raise ValueError(f"expected yes or no, not {value}")


def _strbool_marshal(value: bool) -> str:
    return "yes" if value else "no"


def _intbool_parse(value: str) -> bool:
    match value:
        case "1":
            return True
        case "0":
            return False
        case _:
            raise ValueError(f"expected 0 or 1, not {value}")


def _intbool_marshal(value: bool) -> str:
    return "1" if value else "0"


def _make_sep_callback(sep: str) -> Callback:
    r"""Make callback based on a given separator character.

    Args:
        sep: Separator character to generate parser and marshaller with.

    Examples:
        `_make_sep_callback(":")`
            Make a callback that will split a string on a colon (":")

        `_make_sep_callback(",")`
            Make a callback that will split a string on a comma (",")
    """

    def _sep_parser(value: str) -> list[Any]:
        return [_autocast(v) for v in value.split(sep)]

    def _sep_marshaller(value: Iterable[Any]) -> str:
        return sep.join(str(v) for v in value)

    return make_callback(_sep_parser, _sep_marshaller)


def _make_dict_callback(sep: str, pair_sep: str = "=", array_sep: str | None = None) -> Callback:
    r"""Make a callback based on given dictionary separators.

    Args:
        sep: Separator character used for separating key, value pairs.
        pair_sep: Separator character used for separating keys and values.
        array_sep: Separator character used for lists/arrays.

    Examples:
        `_make_dict_callback(",", "=", ",")`:
            Make a callback that will split the dictionary on a comma (","),
            split the key value pairs on equals sign ("="), and split array
            values on a comma (",").
    """

    def _dict_parser(value: str) -> dict[str, Any]:
        result: dict[str, Any] = {}

        for pair in value.split(sep):
            if pair_sep not in pair:
                result[pair] = True
                continue

            k, v = pair.split(pair_sep, maxsplit=1)
            if array_sep is not None and array_sep in v:
                result[k] = [_autocast(v_) for v_ in v.split(array_sep)]
            else:
                result[k] = _autocast(v)

        return result

    def _dict_marshaller(value: Mapping[str, Any]) -> str:
        result: list[str] = []

        for k, v in value.items():
            if isinstance(v, bool):
                # If `v` is `False`, omit `k` from final marshaled output.
                if v:
                    result.append(k)

                continue

            if array_sep is not None and isinstance(v, Iterable) and not isinstance(v, str):
                v = array_sep.join(str(v_) for v_ in v)

            result.append(f"{k}{pair_sep}{v}")

        return sep.join(result)

    return make_callback(_dict_parser, _dict_marshaller)


DefaultCallback = make_callback(_autocast, lambda v: str(v))
QuoteCallback = make_callback(_autocast, lambda v: f'"{v}"')
MultilineCallback = make_callback(_autocast, lambda v: "\n".join(v))
BoolCallback = make_callback(_bool_parse, _bool_marshal)
StrBoolCallback = make_callback(_strbool_parse, _strbool_marshal)
IntBoolCallback = make_callback(_intbool_parse, _intbool_marshal)
CommaDictCallback = _make_dict_callback(",", "=", ",")
CommaDictColonPairCallback = _make_dict_callback(",", ":", ",")
CommaDictColonArrayCallback = _make_dict_callback(",", "=", ":")
SemicolonDictCallback = _make_dict_callback(";", "=", ",")
ColonSepCallback = _make_sep_callback(":")
CommaSepCallback = _make_sep_callback(",")
