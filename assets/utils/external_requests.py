import time
import requests
from random import random
from typing import Union


def external_get_request(
    url: str, headers: dict, timeout: int = 10, sleep: float = 0.5, timeout_retries: int = 2,
) -> Union[dict, list]:
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
        )
        response.raise_for_status()
        body = response.json()

        return body
    except Exception as e:
        if timeout_retries == 0:
            raise e

        time.sleep(sleep)
        return external_get_request(
            url=url,
            headers=headers,
            timeout=timeout,
            sleep=sleep + random(),
            timeout_retries=timeout_retries - 1,
        )
