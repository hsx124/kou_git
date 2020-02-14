from ipdds_app.views.view_main import MainView
from ipdds_app.service.service_03_detail import DetailService
import json
from django.shortcuts import render

class IpDetailView(MainView):

    template_name = 'ipdds_app/03_detail.html'

    #サービスクラス
    detailService = DetailService()

    def get(self, request):
        context ={}
        #サービスの実行
        dto = self.detailService.bizProcess(request.GET.get('ip_code'))
        #javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto)
        #組み込みタグ用
        context['object_to_html'] = dto
        return render(request, self.template_name, context)
