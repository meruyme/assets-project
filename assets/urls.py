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
        'price-history/<int:asset_id>/',
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
