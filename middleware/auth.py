from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleWare(MiddlewareMixin):
    """中间件"""
    # 若方法中没有返回值则返回None继续往后走
    # 若方法中有返回值则执行不往后走
    def process_request(self, request):
        # 排除不需要登陆就能访问的页面
        # request.path_info 获取当前页面url
        if request.path_info in ["/login/", "/image/code/"]:
            return
        # 读取当前访问用户的session信息，若能读到说明登陆过，继续
        info_dict = request.session.get("info")
        if info_dict:
            return
        # 没登陆过
        return redirect('/login/')