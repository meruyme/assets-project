from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef
from django.views.generic import ListView

from assets.models import Asset, AssetPriceHistory


class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    context_object_name = 'assets'
    paginate_by = 10
    template_name = 'assets/list-assets.html'

    def get_queryset(self):
        current_price = AssetPriceHistory.objects.filter(
            asset_id=OuterRef('pk')
        ).order_by('-retrieved_at')

        return Asset.objects.filter(
            user=self.request.user
        ).annotate(
            last_price=current_price.values('price')[:1],
            last_retrieved_at=current_price.values('retrieved_at')[:1],
        ).order_by(
            'name',
        )
