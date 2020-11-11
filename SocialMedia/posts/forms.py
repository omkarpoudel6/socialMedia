from django import forms
from django.contrib.auth import authenticate,get_user_model
from .models import Post


class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self,*args, **kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if username and password:
            user=authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError('This user doesnot exists')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm,self).clean(*args, **kwargs)

class CreatePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','image','content']

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'})
        }
