from django.db import models
from django.conf import settings
from django_celery_beat.models import PeriodicTask, IntervalSchedule, MINUTES

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
        auto_now=False,
    )

    def __str__(self):
        return str(self.pk)

    def save(self, **kwargs):
        super().save(**kwargs)
        self.update_schedule()

    def delete(self, using=None, keep_parents=False):
        self.delete_schedule()
        super().delete(using, keep_parents)

    def get_schedule_task_name(self):
        return f'asset_{self.id}'

    def update_schedule(self):
        interval, _ = IntervalSchedule.objects.get_or_create(every=self.tracking_frequency, period=MINUTES)

        PeriodicTask.objects.update_or_create(
            name=self.get_schedule_task_name(),
            task='assets.tasks.retrieve_asset',
            defaults={
                'interval': interval,
                'enabled': True,
                'args': [self.id],
            },
        )

    def delete_schedule(self):
        PeriodicTask.objects.filter(name=self.get_schedule_task_name()).delete()


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
    market_time = models.DateTimeField()
    retrieved_at = models.DateTimeField(
        verbose_name='Data/hora de monitoramento',
        auto_now_add=True,
        auto_now=False,
    )

    def __str__(self):
        return f'{self.asset_id} - R${self.price}'
