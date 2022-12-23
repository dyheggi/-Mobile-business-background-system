"""
自定义分页组件，以后在使用此分页组件，需要：
视图函数中：
    def pretty_list(request):
        # 1.根据自己情况筛选数据
        queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
                "queryset": page_object.page_queryset,   # 分完页数据
                "page_string": page_object.html()        # 生成页码
            }
        return render(request, "pretty_list.html", context)

在html页面中：
    {% for obj in queryset %}
        {{ obj.xxx }}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
"""


from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 查询的符合条件的数据（需根据此数据进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: URL中传递的获取分页的参数，例如：/pretty/list/?page=6
        :param plus: 显示当前页的前后plus页（页码）
        """
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()  # 数据总条数
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

        self.plus = plus

    def html(self):
        # 计算当前页前plus页后plus页
        if self.total_page_count <= 2 * self.plus:
            # 数据较少，没有2 * plus页
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据较多，大于2 * plus页
            if self.page <= self.plus:
                # 当前页<plus
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页>plus
                if (self.page + self.plus) > self.total_page_count:
                    # 当前页面+plus > 总页面
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])

        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))  # 首页

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 当前
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            back = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            back = '<li><a href="{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(back)

        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))  # 尾页

        search_string = """
            <li>
                        <form style="float: left; margin-left: -1px" method="get">
                        <input type="text" style="position: relative; float: left; display: inline-block; width:80px; border-radius: 0" 
                            name="page" class="form-control" required="required" placeholder="页 码">
                        <button style:"border-radius: 0" class="btn btn-default" type="submit">跳 转</button>
                </form>
            </li>
            """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string