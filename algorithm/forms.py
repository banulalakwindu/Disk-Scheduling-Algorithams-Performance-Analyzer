from django import forms

class InputForm(forms.Form):
    data = forms.CharField(label='Insert the request queue', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'ex: 98 183 37 122 14 124 65 67'}))
    hPos = forms.CharField(label='Insert the head position', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'ex: 53'}))
    sPos = forms.CharField(label='Insert the Start Value', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'ex: 0'}))
    ePos = forms.CharField(label='Insert the End Value', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'ex: 199'}))