from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from horsebox.cli.render import render_error

__PARAM_GROUP_SEPARATOR = '|'
__PARAM_SEPARATOR = ';'
__KEY_VALUE_SEPARATOR = '='
__VALUE_STRING_MARKER = "'"
__VALUE_LIST_BEGIN_MARKER = '['
__VALUE_LIST_END_MARKER = ']'
__VALUE_LIST_SEPARATOR = ','


def build_params_group(params: List[str]) -> str:
    """
    Build parameters from a group of parameters.

    >>> build_params_group(['param1=1', 'param2=2'])
    'param1=1|param2=2'

    >>> build_params_group(['', 'param1=1'])
    '|param1=1'

    Args:
        params (List[str]): The group of parameters.
    """
    return __PARAM_GROUP_SEPARATOR.join(params)


def parse_params_group(
    params: Optional[str],
    expected: int,
) -> List[str]:
    """
    Parse groups of parameters from a string.

    >>> parse_params_group('', 3)
    ['', '', '']

    >>> parse_params_group('param1=1|param2=2', 2)
    ['param1=1', 'param2=2']

    >>> parse_params_group('|param1=1', 2)
    ['', 'param1=1']

    Args:
        params (Optional[str]): The string containing the parameters.
        expected (int): The number of expected groups.
    """
    if params:
        params_group = params.split(__PARAM_GROUP_SEPARATOR)
        if len(params_group) != expected:
            render_error(f'Incorrect number of parameters groups: {params} (expected: {expected})', exit=True)
        else:
            return params_group
    else:
        return [''] * expected

    return []


def parse_params(
    params: Optional[str],
    is_raw: bool = False,
) -> Dict[str, Any]:
    """
    Parse parameters from a string.

    >>> parse_params(None)
    {}

    >>> parse_params('text=lorem;number=123;boolean=true;list=[a,b,c]')
    {'text': 'lorem', 'number': 123, 'boolean': True, 'list': ['a', 'b', 'c']}

    >>> parse_params('list=[a,b,c]', False)
    {'list': ['a', 'b', 'c']}

    >>> parse_params('list=[a,b,c]', True)
    {'list': '[a,b,c]'}

    Args:
        params (Optional[str]): The string containing the parameters.
        is_raw (bool): Whether the value should be returned as is or parsed.
            Default to False.
    """
    if not params:
        return {}

    parsed: Dict[str, Any] = {}

    for param in params.split(__PARAM_SEPARATOR):
        key_val = param.strip().split(__KEY_VALUE_SEPARATOR, 1)
        if len(key_val) != 2:
            render_error(f'Invalid key-value parameter: {param}', exit=True)

        key, value = key_val
        typed_value = value if is_raw else __parse_typed_value(value)
        if typed_value is None:
            render_error(f"Couldn't detect the type of the value: {param}", exit=True)

        parsed[key] = typed_value

    return parsed


def __parse_typed_value(value: str) -> Optional[Union[int, str, bool, List[str]]]:
    """
    Parse a string value to a typed one.

    >>> __parse_typed_value('lorem')
    'lorem'

    >>> __parse_typed_value("'lorem'")
    'lorem'

    >>> __parse_typed_value('TRUE')
    True

    >>> __parse_typed_value('true')
    True

    >>> __parse_typed_value('1234')
    1234

    >>> __parse_typed_value('[a,b,c]')
    ['a', 'b', 'c']

    Args:
        value (str): The string value to parse.
    """
    value = value.strip()

    if value.startswith(__VALUE_LIST_BEGIN_MARKER) and value.endswith(__VALUE_LIST_END_MARKER):
        values = value.strip(__VALUE_LIST_BEGIN_MARKER).strip(__VALUE_LIST_END_MARKER).split(__VALUE_LIST_SEPARATOR)
        return list(
            map(
                lambda v: v.strip(__VALUE_STRING_MARKER),
                values,
            )
        )
    elif value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    elif value.isdigit():
        return int(value)

    return value.strip(__VALUE_STRING_MARKER)
