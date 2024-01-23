from django import forms


class UserInputForm(forms.Form):
    text_input = forms.CharField(
        widget=forms.Textarea,
        label="Give your search for eBay")
