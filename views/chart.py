from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """数据统计"""
    return render(request, "chart_list.html")


def chart_bar(request):
    """构造柱状图数据"""
    # 数据库中获取数据
    legend = ["销量"]

    series_list = [
        {
            "name": '销量',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        }
    ]

    xAxis_list = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "xAxis_list": xAxis_list,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """构造饼状图数据"""
    db_data_list = [
        {"value": 1048, "name": 'Search Engine'},
        {"value": 735, "name": 'Direct'},
        {"value": 580, "name": 'Email'},
        {"value": 484, "name": 'Union Ads'},
        {"value": 300, "name": 'Video Ads'}
    ]
    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    """构造折线图数据"""
    legend = ["上海", "北京"]

    series_list = [
        {
            "name": '上海',
            "type": 'line',
            "stack": 'Total',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '北京',
            "type": 'line',
            "stack": 'Total',
            "data": [10, 25, 40, 5, 15, 25]
        }
    ]

    xAxis_list = ['1月', '2月', '3月', '4月', '5月', '6月']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "xAxis_list": xAxis_list,
        }
    }
    return JsonResponse(result)