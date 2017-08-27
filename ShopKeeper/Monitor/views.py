from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Config import Config
from Inquiry import Inquiry
import traceback


def index(request):
    year_range = range(2016, 2018)
    month_range = range(1, 13)
    day_range = range(1, 32)
    return render(request, 'index.html', locals())


@csrf_exempt
def get_result_for_day(request):
    print request.POST.items()
    if request.method == 'POST':
        post_dic = request.POST
        try:
            if 'day' in post_dic.keys():
                return HttpResponse(Inquiry.get_results_for_day(int(post_dic['year']),
                                                                int(post_dic['month']),
                                                                int(post_dic['day'])))
            else:
                return HttpResponse(Inquiry.get_results_for_month(int(post_dic['year']),
                                                                  int(post_dic['month'])))
        except Exception, e:
            traceback.print_exc()
            return HttpResponse(repr(e))
    return HttpResponse("GET")


@csrf_exempt
def get_result_for_mac(request):
    if request.method == 'GET':
        info = Inquiry.get_result_for_mac_all()
    else:
        info = Inquiry.get_result_for_mac(request.POST['mac'])

    return render(request, 'customers.html', locals())


@csrf_exempt
def config(request):
    if request.method == 'POST':
        Config.alertConfig(request.POST)

    conf = Config.scanConfig()
    return render(request, 'config.html', locals())
