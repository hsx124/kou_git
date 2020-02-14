from ipdds_app.views.view_main import MainView
import json
from django.shortcuts import render
from ipdds_app.service.service_06_similar_search import SimilarSearchService

class SimilarSearchFormView(MainView):
    template_name = 'ipdds_app/06_similar_search.html'

    #サービスクラス
    similarSearchService = SimilarSearchService()

    def get(self, request):

        context ={}

        #サービスの実行
        dto = self.similarSearchService.bizProcess()

        #javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto)
        #組み込みタグ用
        context['object_to_html'] = dto

        return render(request, self.template_name, context)
