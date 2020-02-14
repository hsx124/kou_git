from ipdds_app.views.view_main import MainView
from ipdds_app.service.service_08_link_collection import LinkCollectionService

class LinkCollectionView(MainView):

    template_name = 'ipdds_app/08_link_collection.html'
    #サービスクラス
    searchLinkCollection = LinkCollectionService()

    def get_context_data(self, **kwargs):

        # コンテキストの取得
        context = super().get_context_data(**kwargs)

        #サービスの実行
        dto = self.searchLinkCollection.bizProcess()

        #組み込みタグ用
        context['object_to_html'] = dto

        return context 
