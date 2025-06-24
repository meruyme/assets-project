from django import forms

from assets.models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('name', 'upper_limit', 'lower_limit', 'tracking_frequency')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        upper_limit = self.cleaned_data.get('upper_limit')
        lower_limit = self.cleaned_data.get('lower_limit')

        if upper_limit and lower_limit and upper_limit <= lower_limit:
            self.add_error('upper_limit', 'O limite superior deve ser maior que o inferior.')

        return self.cleaned_data
