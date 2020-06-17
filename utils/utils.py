import random
import string
from enum import Enum
from typing import Any, List


def get_random_value(num_chars: int, chars: str = string.ascii_uppercase, prefix: str = "", postfix: str = "") -> str:
    generated_text = ''.join(random.choice(chars) for _ in range(num_chars))
    return prefix + generated_text + postfix


def get_random_from_list(options: List[Any]) -> Any:
    return random.choice(options)


def get_random_key_from_dict(options: dict) -> str:
    return random.choice(list(options))


def get_random_value_from_enum(options: Enum) -> Any:
    result = random.choice(list(options))
    return result.value
