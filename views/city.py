from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


def city_list(request):
    queryset = models.City.objects.all()
    return render(request, "city_list.html", {"queryset": queryset})


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    title = "新建城市"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()  # 文件自动保存，字段+上传路径写入到数据库
        return redirect("/city/list")
    return render(request, 'upload_form.html', {"form": form, "title": title})