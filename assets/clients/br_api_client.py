from decimal import Decimal
from datetime import datetime
from dateutil import tz

from django.utils import timezone

from assets.utils.external_requests import external_get_request
from django.conf import settings


class BRAPIClient:

    @staticmethod
    def get_current_asset_price(asset_name: str) -> dict:
        url = settings.BR_API_CONFIG['url']
        token = settings.BR_API_CONFIG['token']

        response = external_get_request(
            url=f"{url}quote/{asset_name}?token={token}",
        )

        if not isinstance(response, dict) or len(response.get('results', [])) == 0:
            raise Exception('Price unavailable.')

        retrieved_datetime = datetime.strptime(
            response['results'][0]['regularMarketTime'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=tz.gettz('UTC'))

        return {
            'price': round(Decimal(response['results'][0]['regularMarketPrice']), 2),
            'market_time': timezone.localtime(retrieved_datetime),
        }
