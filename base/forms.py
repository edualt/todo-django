from django import forms
from .models import Task

class PostTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'complete', )

        widgets = {

            'title' : forms.TextInput(attrs={ 'class' : 'form-control' }),
            'description' : forms.TextInput(attrs={ 'class' : 'form-control' }),
            'complete' : forms.CheckboxInput(),
        }
        



