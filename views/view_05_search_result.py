from ipdds_app.views.view_main import MainView
import json
from django.shortcuts import render
from django.http.response import JsonResponse
from ipdds_app.service.service_05_search_result import SearchResultService

class SearchResultFormView(MainView):
    template_name = 'ipdds_app/05_search_result.html'

    #サービスクラス
    searchResultService = SearchResultService()

    def post(self, request):

        context ={}
        #サービスの実行
        dto = self.searchResultService.bizProcess(request.POST)

        if request.is_ajax():
            return JsonResponse(dto)
        else:
            #javascriptデータ連携用
            context['object_to_javascript'] =  json.dumps(dto)
            #組み込みタグ用
            context['object_to_html'] = dto
            return render(request, self.template_name, context)

    def get(self, request):
        context ={}
        #サービスの実行
        dto = self.searchResultService.bizProcess(request.GET)

        #javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto)
        #組み込みタグ用
        context['object_to_html'] = dto
        return render(request, self.template_name, context)
