from datetime import datetime, timezone
from dateutil.parser import parse


def test_expiration():
    end_time = "2024-08-14T17:36:57.467Z"  # in rfc3339
    start_time = "2024-08-14T12:02:59.149Z"  # in rfc3339
    end_time = parse(end_time)
    start_time = parse(start_time)
    print(datetime.now())
    new_start = start_time.astimezone(timezone.utc)
    new_end = end_time.astimezone(timezone.utc)
    now = datetime.now().astimezone(timezone.utc)
    print(new_end - new_start, new_start, new_end, now)
    assert new_start < new_end
    assert new_end > new_start
