# forms.py
import django_filters
from django import forms

from general.models import DocumentFile


class DocumentFileSearchForm(forms.Form):
    title = django_filters.CharFilter(lookup_expr="iexact")
    # title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = DocumentFile
        fields = ["subjects", "languages"]


# class DocumentFileSearchForm(forms.Form):
#     query = forms.CharField(label='Search', max_length=255, required=False)
#
#     subjects = forms.MultipleChoiceField(
#         choices=[],
#         required=False,
#         widget=forms.SelectMultiple
#     )
#
#     languages = forms.MultipleChoiceField(
#         choices=[],
#         required=False,
#         # widget=forms.CheckboxSelectMultiple
#         widget=forms.SelectMultiple
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.fields['subjects'].choices = [(cat, cat) for cat in
#                                            Subject.objects.values_list('name', flat=True).distinct()]
#         self.fields['languages'].choices = [(brand, brand) for brand in
#                                             Language.objects.values_list('name', flat=True).distinct()]
