from django import forms
from .models import Ticket, Review

class TicketModelForm(forms.ModelForm):
    # Title = forms.CharField(max_length=128)
    Description = forms.CharField(widget=forms.Textarea(attrs={'rows':6}))
    class Meta:
        model = Ticket
        fields = ('Title','Description','image')

class ReviewModelForm(forms.ModelForm):
    headline = forms.CharField(max_length=128)
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':6}))
    class Meta:
        model = Review
        fields = ('headline','body','rating')

        