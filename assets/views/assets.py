from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from assets.forms.forms import AssetForm
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


class AssetCreateView(LoginRequiredMixin, CreateView):
    form_class = AssetForm
    success_url = reverse_lazy('assets:list-assets')
    context_object_name = 'asset'
    template_name = 'assets/create-asset.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        messages.success(self.request, 'Ativo cadastrado com sucesso!')

        return HttpResponseRedirect(self.get_success_url())


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AssetForm
    success_url = reverse_lazy('assets:list-assets')
    context_object_name = 'asset'
    template_name = 'assets/update-asset.html'
    queryset = Asset.objects.filter()

    def get_queryset(self):
        return Asset.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Ativo editado com sucesso!')
        return super(AssetUpdateView, self).form_valid(form)


@login_required
def delete_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    asset.delete()

    messages.success(request, 'Ativo excluído com sucesso!')

    return redirect('assets:list-assets')
