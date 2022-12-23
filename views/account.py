from io import BytesIO

from django.shortcuts import render, redirect, HttpResponse
from django import forms

from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01 import models
from app01.utils.code import check_code


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():  # 验证成功，获取用户名密码
        # 验证码校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {"form": form})

        # admin_object = models.Admin.objects.filter(username="", password="").first()
        # 数据库校验
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {"form": form})
        # 验证成功，网站随机生成字符串写到用户浏览器cookie中与session中
        request.session['info'] = {"id": admin_object.id, "name": admin_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/admin/list/')
    return render(request, 'login.html', {"form": form})


def image_code(request):
    """生成图片验证码"""
    # 调用含pillow文件，生成随机图片
    img, code_string = check_code()

    # 写入到session中以便后续获取检验
    request.session['image_code'] = code_string
    # 设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """注销"""
    request.session.clear()
    return redirect("/login/")


