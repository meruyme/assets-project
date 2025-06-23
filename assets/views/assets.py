from django.views.generic import ListView

from assets.models import Asset


class AssetListView(ListView):
    model = Asset
    paginate_by = 10

