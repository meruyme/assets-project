import logging

from assets.clients.br_api_client import BRAPIClient

from assets.models import Asset, AssetPriceHistory
from assets.utils.emails import send_emails
from assetsproject.celery import app

logger = logging.getLogger('retrieve-asset-logger')


@app.task
def retrieve_asset(asset_id):
    logger.info(f"Asset ID {asset_id}: Start monitoring.")
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

    last_asset_price = AssetPriceHistory.objects.filter(
        asset_id=asset_id
    ).exclude(
        id=price_history.id
    ).order_by('retrieved_at').values('price').last()

    logger.info(f"Asset ID {asset_id}: Price created successfully. Asset price history ID: {price_history.id}")

    try:
        if (
            (last_asset_price and last_asset_price['price'] <= asset.upper_limit) or not last_asset_price
        ) and price_history.price > asset.upper_limit:
            email_message = (
                f'O ativo {asset.name} cruzou o limite superior do túnel cadastrado, estando atualmente com o preço '
                f'R${price_history.price}.'
            )

            send_emails(
                emails=[asset.user.email],
                email_subject='Sugestão de venda de ativo',
                email_message=email_message,
            )
            logger.info(f"Asset ID {asset_id}: E-mail sent successfully - Message: {email_message}.")

        elif (
            (last_asset_price and last_asset_price['price'] >= asset.lower_limit) or not last_asset_price
        ) and price_history.price < asset.lower_limit:
            email_message = (
                f'O ativo {asset.name} cruzou o limite inferior do túnel cadastrado, estando atualmente com o preço '
                f'R${price_history.price}.'
            )

            send_emails(
                emails=[asset.user.email],
                email_subject='Sugestão de compra de ativo',
                email_message=email_message,
            )
            logger.info(f"Asset ID {asset_id}: E-mail sent successfully - Message: {email_message}.")
    except Exception as e:
        logger.error(f"Asset ID {asset_id}: Error sending e-mail: {str(e)}.")
