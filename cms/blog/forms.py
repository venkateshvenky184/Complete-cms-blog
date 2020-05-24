from django import forms
import re
from blog.models import Post
from tinymce.widgets import TinyMCE


class ContactForm(forms.Form):
    countries  = [ ("IND","INDIA"),("CHN","CHINA"),]
    name = forms.CharField(max_length=50,widget = forms.TextInput(attrs = {"class":"input-field","placeholder":"Name"}))
    password = forms.CharField(max_length=16,widget = forms.PasswordInput)
    email = forms.EmailField(required = False)
    phone_number = forms.RegexField(regex="^[6-9][0-9]{9}$",label="Phone",error_messages={'Invalid':'Please Enter Indian Number'},required = False)
    message = forms.CharField(max_length=500,widget = forms.Textarea)
    country = forms.ChoiceField(choices=countries,widget=forms.RadioSelect)


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone_number")


        if email == "" and phone == "":
            #raise forms.ValidationError("Atleast email or phone should be provided", code="Invalid")
            self.add_error("email","Atleast email or phone should be provided")

    def clean_password(self):
        password = self.cleaned_data.get("password")   
        m = re.search("[A-Z]",password)   

        if not m:
            raise forms.ValidationError("Atleast one upper case", code="upper")  
        else:
            return password


class Postform(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    author = forms.CharField(disabled=True)

    class Meta:
        model = Post
        fields = ["title","content","status","category","image","author"]


    # def clean_image(self):
    #     image = self.cleaned_data.get("image") 
    #     if image.size > 240000:
    #         # raise forms.ValidationError("Image should be leass than 200KB", code="Size")
    #         self.add_error("image","Image should be leass than 200KB")
    #     else:
    #         return image

