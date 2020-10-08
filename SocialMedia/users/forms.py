from django import forms
from django.contrib.auth import authenticate,get_user_model

User=get_user_model()

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

class UserRegisterForm(forms.ModelForm):
    password2=forms.CharField(widget=forms.PasswordInput,label='Confirm Password')

    class Meta:
        model=User
        fields=['username','email','password','password2']

        widgets={
            'password':forms.PasswordInput
        }

    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_qs=User.objects.filter(email=email)
        if email_qs.exists():
            print("Email is already being used")
            raise forms.ValidationError("This email is already being used")
        return email

    def clean_password2(self):
        password1=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')

        if password1 != password2:
            print("Password don't match")
            raise forms.ValidationError("Password don't match")
        return password2

    def clean_username(self):
        username=self.cleaned_data.get('username')
        username_qs=User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("Username is already Taken")
        return username

