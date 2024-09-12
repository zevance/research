from django import forms
from .models import Grant

class GrantCreateForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = ['amount_of_funding', 'title', 'abstract', 'introduction', 'justification', 
                  'objectives', 'methodology', 'research_dessemination_strategy', 
                  'ethical_considerations', 'budget', 'resume']
        widgets = {
            'amount_of_funding': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control'}),
            'introduction': forms.Textarea(attrs={'class': 'form-control'}),
            'justification': forms.Textarea(attrs={'class': 'form-control'}),
            'objectives': forms.Textarea(attrs={'class': 'form-control'}),
            'methodology': forms.Textarea(attrs={'class': 'form-control'}),
            'research_dessemination_strategy': forms.Textarea(attrs={'class': 'form-control'}),
            'ethical_considerations': forms.Textarea(attrs={'class': 'form-control'}),
            'budget': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.call = kwargs.pop('call', None)
        super(GrantCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(GrantCreateForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
            
        if self.call:
            instance.call = self.call
            
        if commit:
            instance.save()
        return instance

class GrantUpdateForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = ['amount_of_funding', 'title', 'abstract', 'introduction', 'justification', 
                  'objectives', 'methodology', 'research_dessemination_strategy', 
                  'ethical_considerations', 'budget', 'resume']
       
        widgets = {
            'amount_of_funding': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'introduction': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'justification': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'methodology': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'research_dessemination_strategy': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'ethical_considerations': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'budget': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

        def clean_budget(self):
            budget_file = self.cleaned_data['budget']
            if budget_file:
                # Keep only the file name without the path
                return budget_file.name.split('/')[-1]
            return budget_file

        def clean_resume(self):
            resume_file = self.cleaned_data['resume']
            if resume_file:
                # Keep only the file name without the path
                return resume_file.name.split('/')[-1]
            return resume_file
