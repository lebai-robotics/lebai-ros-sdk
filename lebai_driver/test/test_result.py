from lebai_driver.result import fail, ok


def test_ok_result_defaults_to_success():
    result = ok()

    assert result.success is True
    assert result.code == 0
    assert result.message == ''


def test_fail_result_carries_code_and_message():
    result = fail('bad command', code=42)

    assert result.success is False
    assert result.code == 42
    assert result.message == 'bad command'
