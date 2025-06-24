from django.urls import path
from assets.views import AssetListView, AssetCreateView, AssetUpdateView, AssetPriceHistoryListView, delete_asset

app_name = 'assets'

urlpatterns = [
    path(
        '',
        AssetListView.as_view(),
        name='list-assets',
    ),
    path(
        '<int:asset_id>/price-history/',
        AssetPriceHistoryListView.as_view(),
        name='list-assets-price-history',
    ),
    path(
        'create/',
        AssetCreateView.as_view(),
        name='create-asset',
    ),
    path(
        'update/<int:pk>/',
        AssetUpdateView.as_view(),
        name='update-asset',
    ),
    path(
        'delete/<int:pk>/',
        delete_asset,
        name='delete-asset',
    ),
]
