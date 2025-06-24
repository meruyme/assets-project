from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from assets.models import AssetPriceHistory, Asset


class AssetPriceHistoryListView(LoginRequiredMixin, ListView):
    model = AssetPriceHistory
    context_object_name = 'prices_history'
    paginate_by = 10
    template_name = 'assets-price-history/list-assets-price-history.html'

    def get_queryset(self):
        return AssetPriceHistory.objects.filter(
            asset__user=self.request.user, asset_id=self.kwargs['asset_id']
        ).select_related(
            'asset'
        ).order_by(
            '-retrieved_at',
        )

    def get_context_data(self, **kwargs):
        context = super(AssetPriceHistoryListView, self).get_context_data(**kwargs)
        context['asset'] = get_object_or_404(Asset, pk=self.kwargs['asset_id'])
        return context
