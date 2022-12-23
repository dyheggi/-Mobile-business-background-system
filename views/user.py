from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm


def user_list(request):
    # 获取所有用户列表
    queryset = models.UserInfo.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    # for obj in queryset:
    #     print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"),
    #           obj.get_gender_display(), obj.depart.title)
    return render(request, 'user_list.html', context)


def user_add(request):
    if request.method == 'GET':
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, "user_add.html", context)

    # 获取用户提交数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('account')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gender')
    depart_id = request.POST.get('depart')

    # 添加到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=account, create_time=ctime,
                                   gender=gender, depart_id=depart_id)
    return redirect("/user/list/")


def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})
    # 用户post提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    # 根据id去数据库获取编辑行数据
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存用户输入所有数据
        form.save()
        # form.instance.字段名 = 值
        return redirect('/user/list')
    return render(request, 'user_add.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
