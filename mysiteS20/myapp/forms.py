from django import forms
from myapp.models import Order


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
