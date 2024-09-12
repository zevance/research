from django import forms
from .models import Call
    
class CallForApplicationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    # category = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}))
    document = forms.FileField(widget=forms.FileInput(attrs={"class":"form-control"}))
   # widget={'document':forms.FileInput(attrs={'class':'form-control'})}

    class Meta:
        model = Call
        fields = ['name',
                  'category',
                  'document'
                ]