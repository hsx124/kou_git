from ipdds_app.views.view_main import MainView
from ipdds_app.service.service_02_title_search import SearchTitleService
import json

class SearchTitleView(MainView):

    #テンプレート
    template_name = 'ipdds_app/02_title_search.html'
    #サービスクラス
    searchTitleService = SearchTitleService()
   

    def get_context_data(self, **kwargs):

        # コンテキストの取得
        context = super().get_context_data(**kwargs)

        #サービスの実行
        dto = self.searchTitleService.bizProcess()

        #javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto)
        #組み込みタグ用
        context['object_to_html'] = dto

        return context 

