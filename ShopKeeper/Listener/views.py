import json
import thread
import time

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Utils import hdfsOp
from Config import Config

probe_mac = Config.MyConfigParser.get("user_config", "probe_mac")
url = Config.MyConfigParser.get("hdfs_config", "hdfs_url")


# Create your views here.
@csrf_exempt
def home(request):
    if request.method == 'GET':
        return HttpResponse("It works!")
    elif request.method == 'POST':
        # TODO
        # To be separated
        data = request.body[5:]

        now_time = int(time.time())

        data_json = json.loads(data)
        mac_data = data_json['mmac']
        # assert isinstance(mac_data, str)

        if mac_data == probe_mac:
            file_name = str(now_time) + ".json"
            thread.start_new_thread(hdfsOp.save_to_hdfs, (data, file_name))

        return HttpResponse("Post Success")
