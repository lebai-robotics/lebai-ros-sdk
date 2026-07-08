def test_status_access_is_available_when_no_exclusive_call_is_pending():
    from lebai_driver.sdk_gate import StatusServiceGate

    gate = StatusServiceGate()

    with gate.status_access() as enabled:
        assert enabled is True


def test_status_access_skips_while_exclusive_call_is_active():
    from lebai_driver.sdk_gate import StatusServiceGate

    gate = StatusServiceGate()

    with gate.exclusive_access():
        with gate.status_access() as enabled:
            assert enabled is False
