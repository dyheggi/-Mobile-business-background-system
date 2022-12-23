import os

from django.shortcuts import render, HttpResponse
from django.conf import settings
from django import forms

from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from app01 import models


def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    file_object = request.FILES.get('avatar')
    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse("hi")


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 读取文件内容写入文件夹并获取其路径
        img_object = form.cleaned_data.get("img")
        media_path = os.path.join("media", img_object.name)   # 上传的数据在media里拼接
        f = open(media_path, mode='wb')
        for chunk in img_object.chunks():
            f.write(chunk)
        f.close()

        # 将图片内容写入数据库
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=media_path
        )
        return HttpResponse("hi")
    return render(request, 'upload_form.html', {"form": form, "title": title})


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"


def upload_model_form(request):
    """上传文件数据（基于modelform）"""
    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save() # 文件自动保存，字段+上传路径写入到数据库
        return HttpResponse("上传成功")
    return render(request, 'upload_form.html', {"form": form, "title": title})
