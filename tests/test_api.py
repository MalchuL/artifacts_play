import logging
import time

import pytest
from dynaconf import settings
import pprint

logger = logging.getLogger(__name__)


@pytest.mark.slow
def test_api():
    import requests
    char_name = settings.CHARACTERS[0]
    url = f"https://api.artifactsmmo.com/my/{char_name}/action/move"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {settings.API_TOKEN}"
    }
    while True:
        zero_move = requests.post(url, headers=headers, json={"x": 0, "y": 0})  # move to (0, 0)
        logger.info("First try, move to zeros" + pprint.pformat(zero_move.json()))

        if zero_move.status_code == 200:
            remaining_second = zero_move.json()["data"]["cooldown"]["remaining_seconds"]
            time.sleep(remaining_second)
            break
        elif zero_move.status_code == 499:  # Character on cooldown
            time.sleep(5)
        else:
            break

    response = requests.post(url, headers=headers, json={"x": 1, "y": 2})
    logger.info("Move to (1, 2)" + pprint.pformat(response.json()))

    assert response.status_code == 200, response.json()
