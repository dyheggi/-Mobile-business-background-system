from django.shortcuts import render, redirect

from app01 import models
from app01.utils.pagination import Pagination


def admin_list(request):
    """管理员列表"""
    # 检查用户是否登录，若已经登陆继续，若未登录返回登录界面
    # 获取用户请求（cookie随机字符串），检查session中有没有
    info = request.session.get("info")
    if not info:
        return redirect('/login/')


    # 搜素
    data_dict = {}
    search_data = request.GET.get('q')  # 传get实现搜索
    if search_data:
        data_dict["username__contains"] = search_data
    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页数据
        "page_string": page_object.html(),  # 生成页码
    }
    return render(request, "admin_list.html", context)


from django import forms
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致，请重新输入!")
        # 返回的数据会保存在数据库
        return confirm


def admin_add(request):
    """添加管理员"""
    title = "添加管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {"form": form, "title": title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form": form, "title": title})


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


def admin_edit(request, nid):
    # 对象/none
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在"})
    title = "编辑管理员"
    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def admin_delete(request, nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        # 数据库校验当前密码与新输入密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前的密码相同!")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致，请重新输入!")
        # 返回的数据会保存在数据库
        return confirm


def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在"})

    title = "重置密码 - {}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form": form, "title": title})