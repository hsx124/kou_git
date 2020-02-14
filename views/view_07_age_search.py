from ipdds_app.views.view_main import MainView
from ipdds_app.service.service_07_age_search import SearchAgeService
import json

class SearchAgeView(MainView):

    #テンプレート
    template_name = 'ipdds_app/07_age_search.html'
    #サービスクラス
    SearchAgeService = SearchAgeService()

    def get_context_data(self, **kwargs):

        # コンテキストの取得
        context = super().get_context_data(**kwargs)

        #サービスの実行
        dto = self.SearchAgeService.bizProcess()

        #javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto)
        #組み込みタグ用
        context['object_to_html'] = dto

        return context
