from django.db import models
from django.conf import settings

from assets.utils.validators import GreaterThanValueValidator


class Asset(models.Model):
    name = models.CharField(
        verbose_name='Nome',
        max_length=255,
    )
    upper_limit = models.DecimalField(
        verbose_name='Limite superior',
        max_digits=10,
        decimal_places=2,
        validators=[GreaterThanValueValidator(0)],
    )
    lower_limit = models.DecimalField(
        verbose_name='Limite inferior',
        max_digits=10,
        decimal_places=2,
        validators=[GreaterThanValueValidator(0)],
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        on_delete=models.CASCADE,
        related_name='assets',
    )
    tracking_frequency = models.PositiveSmallIntegerField(
        verbose_name='Frequência de monitoramento (em minutos)',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        auto_now=False
    )

    def __str__(self):
        return str(self.pk)


class AssetPriceHistory(models.Model):
    asset = models.ForeignKey(
        Asset,
        verbose_name='Ativo',
        on_delete=models.CASCADE,
        related_name='price_history',
    )
    price = models.DecimalField(
        verbose_name='Cotação',
        max_digits=10,
        decimal_places=2,
        validators=[GreaterThanValueValidator(0)],
    )
    retrieved_at = models.DateTimeField(
        verbose_name='Data/hora de monitoramento',
    )

    def __str__(self):
        return f'{self.asset_id} - R${self.price}'
