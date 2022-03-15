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
        
class CreateUserForm(UserCreationForm):
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
