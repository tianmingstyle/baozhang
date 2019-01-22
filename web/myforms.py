# codint:utf-8
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
from repository.models import User


class MyForm(Form):
    user = fields.CharField(max_length=32)
    pwd = fields.CharField(max_length=32)
    pwdconfirm = fields.CharField(max_length=32)
    email = fields.EmailField()
    img = fields.ImageField()

    def clean_user(self):
        user = self.cleaned_data['user']
        if User.objects.filter(username=user).exists():
            raise ValidationError('%s exists....' % user)
        return user

    def clean(self):
        pwd = self.cleaned_data['pwd']
        pwdconfirm = self.cleaned_data['pwdconfirm']
        if pwd != pwdconfirm:
            raise ValidationError('passwords you input are not equal... ')
        return self.cleaned_data


class MyLoginForm(Form):
    user = fields.CharField(max_length=32)
    pwd = fields.CharField(max_length=32)

    def clean_user(self):
        user = self.cleaned_data['user']
        user_obj = User.objects.filter(username=user)
        if user_obj.exists():
            return user

    def clean(self):
        user = self.cleaned_data['user']
        user_obj = User.objects.filter(username=user)
        if user_obj.exists():
            # user_obj = User.objects.filter(username=user)[0]
            # print(user_obj)
            if self.cleaned_data['pwd'] == user_obj[0].pwd:
                return self.cleaned_data
            else:
                raise ValidationError("%s' pwd is wrong...." % user)
