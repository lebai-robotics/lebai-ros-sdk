import pytest
from lebai_interfaces.msg import Result


@pytest.mark.parametrize('message', ['', 'command accepted'])
def test_ok_returns_generated_success_result(message):
    from lebai_driver.result import ok

    result = ok(message) if message else ok()

    assert isinstance(result, Result)
    assert result.success is True
    assert result.code == 0
    assert result.message == message


def test_fail_defaults_to_error_code_one():
    from lebai_driver.result import fail

    result = fail('bad command')

    assert isinstance(result, Result)
    assert result.success is False
    assert result.code == 1
    assert result.message == 'bad command'


def test_fail_carries_explicit_unsupported_code():
    from lebai_driver.errors import UNSUPPORTED
    from lebai_driver.result import fail

    result = fail('unsupported by installed pylebai', code=UNSUPPORTED)

    assert result.success is False
    assert result.code == 2
    assert result.message == 'unsupported by installed pylebai'


@pytest.mark.parametrize(
    'error, expected', [(ValueError('bad command'), 'bad command'), (RuntimeError(), 'RuntimeError')]
)
def test_exception_message_uses_class_name_only_for_empty_text(error, expected):
    from lebai_driver.errors import exception_message

    assert exception_message(error) == expected
