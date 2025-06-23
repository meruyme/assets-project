import logging

from assets.clients.br_api_client import BRAPIClient

from assets.models import Asset, AssetPriceHistory
from assets.utils.emails import send_emails
from assetsproject.celery import app


logging.basicConfig(
    filename="processor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@app.task
def retrieve_asset(asset_id):
    asset = Asset.objects.filter(id=asset_id).select_related('user').first()

    if not asset:
        logger.error(f"Asset ID {asset_id}: Asset not found.")
        return

    try:
        asset_data = BRAPIClient.get_current_asset_price(asset.name)
    except Exception as e:
        logger.error(f"Asset ID {asset_id}: BRAPI error: {str(e)}.")
        return

    price_history = AssetPriceHistory.objects.create(
        asset=asset,
        price=asset_data['price'],
        market_time=asset_data['market_time'],
    )

    try:
        if price_history.price > asset.upper_limit:
            send_emails(
                emails=[asset.user.email],
                email_subject='Vende ai pai',
                email_message='Vende ai pai',
            )

        elif price_history.price < asset.lower_limit:
            send_emails(
                emails=[asset.user.email],
                email_subject='Compra ai pai',
                email_message='Compra ai pai',
            )
    except Exception as e:
        logger.error(f"Asset ID {asset_id}: Error sending e-mail: {str(e)}.")
