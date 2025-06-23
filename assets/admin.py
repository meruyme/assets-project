from django.contrib import admin

from assets.models import Asset, AssetPriceHistory


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'tracking_frequency',)
    search_fields = ('name', 'user_id',)


@admin.register(AssetPriceHistory)
class AssetPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('asset', 'price', 'retrieved_at',)
    search_fields = ('asset__name', 'asset_id',)
