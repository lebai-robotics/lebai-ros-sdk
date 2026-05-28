from lebai_interfaces.msg import Result


def ok(message=''):
    return Result(success=True, code=0, message=message)


def fail(message, code=1):
    return Result(success=False, code=code, message=message)
