import json
from django.http.response import JsonResponse
from django.shortcuts import render
from ipdds_app.views.view_main import MainView
from ipdds_app.service.service_03_detail.service_10301_detail import DetailService

class SakuhinDetailView(MainView):

    template_name = 'ipdds_app/03_detail/10301_detail.html'

    #サービスクラス
    detailService = DetailService()

    def get(self, request):
        if request.is_ajax():
            dto = self.ajax(request)
            return JsonResponse(dto, safe=False)
        else:
            context ={}
            #サービスの実行
            dto = self.detailService.bizProcess(request.GET.get('sakuhin_code'))
            #javascriptデータ連携用
            context['object_to_javascript'] =  json.dumps(dto)
            #組み込みタグ用
            context['object_to_html'] = dto
        return render(request, self.template_name, context)

    def ajax(self,request):
        #サービスの実行
        process_code = request.GET.get('process_code')
        if "01-01" == process_code:
            # 掲載媒体情報の取得
            dto = self.detailService.getBunrui(request.GET.get('sakuhin_code'))
        elif "01-02" == process_code:
            # 掲載媒体情報の取得
            dto = self.detailService.getMedia(request.GET.get('sakuhin_code'))
        elif "01-03" == process_code:
            # コア情報の取得
            dto = self.detailService.getCore(request.GET.get('sakuhin_code'))
        elif "01-04" == process_code:
            # タグ情報の取得
            dto = self.detailService.getTag(request.GET.get('sakuhin_code'))
        elif "01-05" == process_code:
            # 類似作品情報の取得
            dto = self.detailService.getRuiji(request.GET.get('sakuhin_code'),json.loads(request.GET.get('tag_code_list')))
        elif "02" == process_code:
            # アニメ情報の取得
            dto = self.detailService.getAnime(request.GET.get('sakuhin_code'))
        elif "03" == process_code:
            # 年代別男女比情報の取得
            dto = self.detailService.getGenderRatio(request.GET.get('sakuhin_code'))
        elif "04-01" == process_code:
            # コードの取得
            dto = self.detailService.getHeibai(request.GET.get('sakuhin_code'))
        elif "04-02" == process_code:
            # 併売情報の取得
            dto = self.detailService.getHeibaiData(request.GET.get('title_code'))
        elif "05" == process_code:
            # 関連文書の取得
            dto = self.detailService.getRelatedDocuments(request.GET.get('sakuhin_code'))
        elif "06-01" == process_code:
            # マンガの取得
            dto = self.detailService.getManga(request.GET.get('sakuhin_code'))
        elif "06-02" == process_code:
            # マンガ基本情報の取得
            dto = self.detailService.getMangaData(request.GET.get('title_code'))
        elif "06-03" == process_code:
            # マンガ実績情報の取得
            dto = self.detailService.getMangaIsbnData(request.GET.get('title_code'))
        elif "06-04" == process_code:
            # マンガグラフ用データの取得
            dto = self.detailService.getMangaGraphData(request.GET.get('title_code'))
        elif "07-01" == process_code:
            # twitterの取得
            dto = self.detailService.getTwitterDataBySakuhinCode(request.GET.get('sakuhin_code'))
        elif "07-02" == process_code:
            # twitter実績の取得
            dto = self.detailService.getTwitterDataByTwitterId(request.GET.get('twitter_id'))
        elif "07-03" == process_code:
            # twitterグラフ用データの取得
            dto = self.detailService.getTwitterGraphDataByTwitterId(request.GET.get('twitter_id'))
        elif "08-01" == process_code:
            # gameの取得
            dto = self.detailService.getGameBySakuhinCode(request.GET.get('sakuhin_code'))
        elif "08-02" == process_code:
            # game実績の取得
            dto = self.detailService.getGameDataByTitleCode(request.GET.get('title_code'))
        elif "08-03" == process_code:
            # gameグラフ用データの取得
            dto = self.detailService.getGameGraphDataByTitleCode(request.GET.get('title_code'))
        elif "09-01" == process_code:
            # appの取得
            dto = self.detailService.getAppBySakuhinData(request.GET.get('sakuhin_code'))
        elif "09-02" == process_code:
            # app実績の取得
            dto = self.detailService.getAppDataByTitleCode(request.GET.get('title_code'),request.GET.get('app_id_ios'),request.GET.get('app_id_android'))
        elif "09-03" == process_code:
            # appグラフ用データの取得(ダウンロード数)
            dto = self.detailService.getAppGraphDataForDownload(request.GET.get('app_id_ios'),request.GET.get('app_id_android'))
        elif "09-04" == process_code:
            # appグラフ用データの取得(収益)
            dto = self.detailService.getAppGraphDataForMonthlySales(request.GET.get('app_id_ios'),request.GET.get('app_id_android'))
        return dto