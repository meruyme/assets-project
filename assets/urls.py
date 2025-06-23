from django.urls import path
from assets.views import AssetListView

app_name = 'assets'

urlpatterns = [
    path(
        '',
        AssetListView.as_view(),
        name='list-assets',
    ),
]
