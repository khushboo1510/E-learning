from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import CheckboxSelectMultiple, PasswordInput
from myapp.models import Order, Student
from passlib.ifc import PasswordHash


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']
        widgets = {
            'student': forms.RadioSelect,
            'order_date': forms.SelectDateWidget(attrs={'class': 'years=date.today()'},
                                                 empty_label=("Year", "Month", "Day"))
        }
        labels = {
            'student': 'Student Name',
            'order_date': 'Order Date'
        }


class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('1', 'Yes'), ('0', 'No')])
    levels = forms.IntegerField(initial=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # do not require password confirmation
        del self.fields['password2']

    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'city', 'interested_in']

        widgets = {
            'interested_in': forms.CheckboxSelectMultiple,
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'interested_in': 'Interested In'
        }
