from django import forms
from django.forms.widgets import SelectDateWidget

from .models import Newspaper


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', required=False)


class NewspaperCreateForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = "__all__"
        widgets = {
            'published_date': SelectDateWidget(),
        }
