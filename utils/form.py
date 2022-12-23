from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm
from django import forms


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=1, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

        # widgets = {
        #     "names": forms.TextInput(attrs={"class": "form-control"})
        # }


class PrettyModelForm(BootStrapModelForm):
    # 验证方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1\d{10}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    # 验证方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        # 验证通过返回信息
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1\d{10}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def clean_mobile(self):
        # print(self.instance.pk) # 打印当前编辑的id
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        # 验证通过返回信息
        return txt_mobile