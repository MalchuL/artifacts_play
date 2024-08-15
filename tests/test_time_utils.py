from src.utils import estimate_moving_time


def test_time_utils():
    start = 9, 8
    end = 3, 1
    target_time = 65
    time = estimate_moving_time(*start, *end)
    assert time == target_time
