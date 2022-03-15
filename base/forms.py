from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'image', 'complete' )

        widgets = {

            'title' : forms.TextInput(attrs={ 'class' : 'form-control' }),
            'description' : forms.TextInput(attrs={ 'class' : 'form-control' }),
            'complete' : forms.CheckboxInput(),
        }
        

