import math


def amplitude_to_gripper_joint(amplitude):
    if not 0.0 <= amplitude <= 100.0:
        raise ValueError('amplitude must be in the range [0, 100]')
    return math.pi / 3.0 * amplitude / 100.0


def parse_six_numbers(value):
    numbers = [float(item) for item in value.split(',')]
    if len(numbers) != 6 or not all(map(math.isfinite, numbers)):
        raise ValueError('expected six comma-separated finite numbers')
    return numbers


def checked_response(service, response):
    if not response.result.success:
        raise RuntimeError(f'{service} failed ({response.result.code}): {response.result.message}')
    return response
