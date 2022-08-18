from django import forms
from django.contrib.auth.forms import UserCreationForm


from Home.models import MyUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    date_of_birth = forms.DateField()
    phone_no = forms.CharField(min_length=10,max_length=10)
    national_id=forms.CharField(min_length=10,max_length=10)
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    
    class Meta:
        model = MyUser
        fields = ['username', 'email','date_of_birth','phone_no' ,'national_id','password1', 'password2']