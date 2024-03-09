from django import forms


class NoResizeTextarea(forms.Textarea):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs.update({'style': 'resize:none; overflow-y:hidden; width 100%; height: 80px;'})
        super().__init__(attrs=attrs)


class UserInputForm(forms.Form):
    text_input = forms.CharField(
        widget=NoResizeTextarea(attrs={
            'rows': 2, 'cols': 30,
            'placeholder': 'Entrez votre recherche eBay ici...',
        }),
        required=False,
    )
