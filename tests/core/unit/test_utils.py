from src.core.utils import (
    get_substring_before_chars,
    get_substring_after_chars
)


def test_get_substring_before_chars_common_case() -> None:
    expected_result: str = 'someString'
    chars: str = '_'
    test_string: str = f'{expected_result}{chars}postfix'
    assert get_substring_before_chars(string=test_string, chars=chars) == expected_result


def test_get_substring_before_chars_without_selected_chars_in_string() -> None:
    chars: str = '_'
    test_string: str = 'Some text without selected symbol'
    assert get_substring_before_chars(string=test_string, chars=chars) == test_string


def test_get_substring_after_chars_common_case() -> None:
    expected_result: str = 'someString'
    chars: str = '_'
    test_string: str = f'prefix{chars}{expected_result}'
    assert get_substring_after_chars(string=test_string, chars=chars) == expected_result


def test_get_substring_after_chars_without_selected_chars_in_string() -> None:
    chars: str = '_'
    test_string: str = 'Some text without selected symbol'
    assert get_substring_after_chars(string=test_string, chars=chars) == test_string
