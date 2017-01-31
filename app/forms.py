# -*- coding: utf-8 -*-

"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from app.models import Client, Employee,  ApplicationType


class CustomAuthenticationForm(AuthenticationForm):
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': u'логін або email'}))
    password = forms.CharField(label=_(u"Ваш пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': u'пароль'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A custom form that lets a user change their password by entering their old
    password.
    """
    old_password = forms.CharField(label=_(u"Поточний пароль"),
                                   widget=forms.PasswordInput(
                                       {
                                           'class': 'form-control',
                                           'placeholder': u'поточний пароль'
                                       }
                                   ))
    new_password1 = forms.CharField(label=_(u"Новий пароль"),
                                    widget=forms.PasswordInput(
                                        {
                                            'class': 'form-control',
                                            'placeholder': u'новий пароль'
                                        }
                                    ))
    new_password2 = forms.CharField(label=_(u"Повторіть новий пароль"),
                                    widget=forms.PasswordInput(
                                        {
                                            'class': 'form-control',
                                            'placeholder': u'новий пароль ще раз'
                                        }
                                    ))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class ClientProfileForm(forms.ModelForm):
    """Client Profile form"""
    class Meta:
        model = Client
        exclude = (
            'user',
            'category',
            'balance',
            'code_1c',
            'deprecated',
        )


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = (
            'user',
            'email_verified',
            'deprecated',
        )


class GeneralAppForm(forms.Form):
    contact_person = forms.CharField(max_length=40)
    contact_phone = forms.CharField(max_length=40)
    text_text = forms.CharField(max_length=1000, widget=forms.Textarea)
    app_scan = forms.FileField()
    app_attach = forms.FileField(required=False)
