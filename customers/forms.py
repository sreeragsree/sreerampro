from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        error_messages={
            'required': 'Phone number is required',
            'min_length': 'Phone number must be 10 digits',
            'max_length': 'Phone number must be 10 digits',
        }
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('Phone number is required')
        if not phone.isdigit():
            raise forms.ValidationError('Phone number must contain only digits')
        if not len(phone) == 10:
            raise forms.ValidationError('Phone number must be 10 digits')
        if not phone[0] in '6789':
            raise forms.ValidationError('Phone number must start with 6, 7, 8, or 9')
        return phone

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


        phone = self.cleaned_data.get('phone')
        # Check if phone matches Indian 10-digit mobile number format
        if not re.match(r'^[6-9]\d{9}$', phone):
            raise forms.ValidationError("Enter a valid 10-digit Indian mobile number starting with 6-9.")
        return phone

def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        

        