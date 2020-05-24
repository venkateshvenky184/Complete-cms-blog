from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
from account.models import User,Profile

class SignUpForm(UserCreationForm):


    # email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ('username','password1','password2','email','first_name','last_name')




# User update form allows users to update user name and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Profile update form allows users to update image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']        