from shedule_app import models as md
from django import forms
import re

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = md.User
        fields = '__all__'

    def is_valid_phone_number(self, phone_number):
        pattern = r"8\(\d{3}\)-\d{3}-\d{2}-\d{2}"
        return bool(re.fullmatch(pattern, phone_number))
    
    def format_phone_number(self, phone_number):
        phone_number = phone_number.replace("(", "")
        phone_number = phone_number.replace(")", "")
        phone_number = phone_number.replace("-", "")
        phone_number = phone_number.replace(" ", "")
        return phone_number

    def clean(self):
        cleaned_data = self.cleaned_data
        tel_number = cleaned_data.get('tel_number')
        if tel_number:
            if self.is_valid_phone_number(tel_number):
                tel_number = self.format_phone_number(tel_number)
                cleaned_data['tel_number'] = int(tel_number)
            if not tel_number.isdigit():
                raise forms.ValidationError(u"Поле номера телефона должно содержать только цифры.")
            if len(tel_number) != 11:
                raise forms.ValidationError(u"Кажется в номере телефона не хватает цифры.")
        return cleaned_data