<<<<<<< HEAD:web/web-front/ipdds/ipdds_app/views/view_04_compare.py
from ipdds_app.views.view_main import MainView
from django.http.response import JsonResponse
from ipdds_app.service.service_04_compare import IpCompareService
import json
from django.shortcuts import render

class IpCompareView(MainView):

    template_name = 'ipdds_app/04_compare.html'

    #サービスクラス
    ipCompareService = IpCompareService()

    def get(self, request):

        if request.is_ajax():
            #非同期通信処理
            return self.ajax(request)
        else:
            #画面初期表示処理
            return self.initialize(request)

    def initialize(self, request):
        context ={}
        #サービスの実行
        #sessionからデータを取得
        ipCodeList = []
        if 'compare_kago' in request.session:
            compare_kago = request.session['compare_kago']
            for ipInfo in compare_kago:
                ipCodeList.append(ipInfo["ip_code"])

        # session にデータ存在する場合
        if ipCodeList:
            dto = self.ipCompareService.bizProcess(ipCodeList)
        # sessionにデータ存在しない場合
        else:
            dto = {'no_session_data':True}
    
        #javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto)
        #組み込みタグ用
        context['object_to_html'] = dto
        return render(request, self.template_name, context)


    def ajax(self, request):
        # 年代別男女比のグラフajax
        if 'gender-ratio' in request.GET:
            return self.get_gender_ratio(request)
        # Twitterのグラフajax
        if 'twitter' in request.GET:
            return self.get_twitter(request)
        # マンガのグラフ１とグラフ２ajax
        if 'book1' in request.GET:
            return self.get_book1(request)
        # マンガのグラフ3とグラフ6 ajax
        if 'book3' in request.GET:
            return self.get_book3(request)
        # マンガのグラフ4 ajax
        if 'book4' in request.GET:
            return self.get_book4(request)
        # マンガのグラフ5 ajax
        if 'book5' in request.GET:
            return self.get_book5(request)
        # ゲームのグラフ1 ajax
        if 'game1' in request.GET:
            return self.get_game1(request)
        # ゲームのグラフ2 ajax
        if 'game2' in request.GET:
            return self.get_game2(request)
        # アプリ売上のグラフ1 ajax
        if 'appSales1' in request.GET:
            return self.get_appSales1(request)
        # アプリ売上のグラフ2 ajax
        if 'appSales2' in request.GET:
            return self.get_appSales2(request)
        # アプリ平均売上と平均ダウンロード数 ajax
        if 'appAvg' in request.GET:
            return self.get_appAvgSales_download(request)
        # アプリダウンロードのグラフ1 ajax
        if 'appDownload1' in request.GET:
            return self.get_appDownload1(request)
        # アプリダウンロードのグラフ2 ajax
        if 'appDownload2' in request.GET:
            return self.get_appDownload2(request)

    def get_gender_ratio(self, request):
        dto = self.ipCompareService.get_gender_ratio(request.GET.get('ip-code'))
        return JsonResponse(dto, safe=False)
    
    def get_twitter(self, request):
        dto = self.ipCompareService.get_twitter(request.GET.get('twitter_id'))
        return JsonResponse(dto, safe=False)

    def get_book1(self, request):
        dto = self.ipCompareService.get_book1(request.GET.get('book_id'))
        return JsonResponse(dto, safe=False)

    def get_book3(self, request):
        dto = self.ipCompareService.get_book3(request.GET.get('book_id'))
        return JsonResponse(dto, safe=False)

    def get_book4(self, request):
        dto = self.ipCompareService.get_book4(request.GET.get('book_id'))
        return JsonResponse(dto, safe=False)

    def get_book5(self, request):
        dto = self.ipCompareService.get_book5(request.GET.get('book_id'))
        print(dto)
        print(json.dumps(dto))
        return JsonResponse(dto, safe=False)

    def get_game1(self, request):
        dto = self.ipCompareService.get_game1(request.GET.get('game_soft_code'))
        return JsonResponse(dto, safe=False)

    def get_game2(self, request):
        dto = self.ipCompareService.get_game2(request.GET.get('game_soft_code'))
        return JsonResponse(dto, safe=False)

    def get_appSales1(self, request):
        dto = self.ipCompareService.get_appSales1(request.GET.get('app_name'))
        return JsonResponse(dto, safe=False)

    def get_appSales2(self, request):
        dto = self.ipCompareService.get_appSales2(request.GET.get('app_name'))
        return JsonResponse(dto, safe=False) 

    def get_appAvgSales_download(self, request):
        dto = self.ipCompareService.get_appAvgSales_download(request.GET.get('app_name'))
        return JsonResponse(dto, safe=False)      

    def get_appDownload1(self, request):
        dto = self.ipCompareService.get_appDownload1(request.GET.get('app_name'))
        return JsonResponse(dto, safe=False)

    def get_appDownload2(self, request):
        dto = self.ipCompareService.get_appDownload2(request.GET.get('app_name'))
=======
from ipdds_app.views.view_main import MainView
from django.http.response import JsonResponse
from ipdds_app.service.service_04_compare.service_10401_compare import SakuhinCompareService
import json
from django.shortcuts import render

class SakuhinCompareView(MainView):

    template_name = 'ipdds_app/04_compare/10401_compare.html'

    #サービスクラス
    SakuhinCompareService = SakuhinCompareService()

    def get(self, request):

        if request.is_ajax():
            #非同期通信処理
            return self.ajax(request)
        else:
            #画面初期表示処理
            return self.initialize(request)

    def initialize(self, request):
        context ={}
        #サービスの実行
        #sessionからデータを取得
        sakuhinCodeList = []
        if 'compare_kago' in request.session:
            compare_kago = request.session['compare_kago']
            for sakuhinInfo in compare_kago:
                sakuhinCodeList.append(sakuhinInfo['sakuhin_code'])

        # session にデータ存在する場合
        if sakuhinCodeList:
            dto = self.SakuhinCompareService.bizProcess(sakuhinCodeList)
        # sessionにデータ存在しない場合
        else:
            dto = {'no_session_data':True}
    
        #javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto)
        #組み込みタグ用
        context['object_to_html'] = dto
        return render(request, self.template_name, context)


    def ajax(self, request):
        # 年代別男女比のグラフajax
        if 'gender-ratio' in request.GET:
            return self.get_gender_ratio(request)
        # Twitterのグラフajax
        if 'twitter' in request.GET:
            return self.get_twitter(request)
        # マンガのグラフ１とグラフ２ajax
        if 'manga1' in request.GET:
            return self.get_manga1(request)
        # マンガのグラフ3とグラフ6 ajax
        if 'manga3' in request.GET:
            return self.get_manga3(request)
        # マンガのグラフ4 ajax
        if 'manga4' in request.GET:
            return self.get_manga4(request)
        # マンガのグラフ5 ajax
        if 'manga5' in request.GET:
            return self.get_manga5(request)
        # ゲームのグラフ1 ajax
        if 'game1' in request.GET:
            return self.get_game1(request)
        # ゲームのグラフ2 ajax
        if 'game2' in request.GET:
            return self.get_game2(request)
        # アプリ売上のグラフ1 ajax
        if 'appSales1' in request.GET:
            return self.get_appSales1(request)
        # アプリ売上のグラフ2 ajax
        if 'appSales2' in request.GET:
            return self.get_appSales2(request)
        # アプリ平均売上と平均ダウンロード数 ajax
        if 'appAvg' in request.GET:
            return self.get_appAvgSales_download(request)
        # アプリダウンロードのグラフ1 ajax
        if 'appDownload1' in request.GET:
            return self.get_appDownload1(request)
        # アプリダウンロードのグラフ2 ajax
        if 'appDownload2' in request.GET:
            return self.get_appDownload2(request)

    def get_gender_ratio(self, request):
        dto = self.SakuhinCompareService.get_gender_ratio(request.GET.get('sakuhin_code'))
        return JsonResponse(dto, safe=False)
    
    def get_twitter(self, request):
        dto = self.SakuhinCompareService.get_twitter(request.GET.get('twitter_id'))
        return JsonResponse(dto, safe=False)

    def get_manga1(self, request):
        dto = self.SakuhinCompareService.get_manga1(request.GET.get('manga_code'))
        return JsonResponse(dto, safe=False)

    def get_manga3(self, request):
        dto = self.SakuhinCompareService.get_manga3(request.GET.get('manga_code'))
        return JsonResponse(dto, safe=False)

    def get_manga4(self, request):
        dto = self.SakuhinCompareService.get_manga4(request.GET.get('manga_code'))
        return JsonResponse(dto, safe=False)

    def get_manga5(self, request):
        dto = self.SakuhinCompareService.get_manga5(request.GET.get('manga_code'))
        return JsonResponse(dto, safe=False)

    def get_game1(self, request):
        dto = self.SakuhinCompareService.get_game1(request.GET.get('game_title_code'))
        return JsonResponse(dto, safe=False)

    def get_game2(self, request):
        dto = self.SakuhinCompareService.get_game2(request.GET.get('game_title_code'))
        return JsonResponse(dto, safe=False)

    def get_appSales1(self, request):
        dto = self.SakuhinCompareService.get_appSales1(request.GET.get('app_title_code'),request.GET.get('app_title_name'),request.GET.get('app_id_ios'),request.GET.get('app_id_android'))
        return JsonResponse(dto, safe=False)

    def get_appSales2(self, request):
        dto = self.SakuhinCompareService.get_appSales2(request.GET.get('app_title_code'),request.GET.get('app_title_name'),request.GET.get('app_id_ios'),request.GET.get('app_id_android'))
        return JsonResponse(dto, safe=False) 

    def get_appAvgSales_download(self, request):
        dto = self.SakuhinCompareService.get_appAvgSales_download(request.GET.get('app_title_code'),request.GET.get('app_title_name'),request.GET.get('app_id_ios'),request.GET.get('app_id_android'))
        return JsonResponse(dto, safe=False)      

    def get_appDownload1(self, request):
        dto = self.SakuhinCompareService.get_appDownload1(request.GET.get('app_title_code'),request.GET.get('app_title_name'),request.GET.get('app_id_ios'),request.GET.get('app_id_android'))
        return JsonResponse(dto, safe=False)

    def get_appDownload2(self, request):
        dto = self.SakuhinCompareService.get_appDownload2(request.GET.get('app_title_code'),request.GET.get('app_title_name'),request.GET.get('app_id_ios'),request.GET.get('app_id_android'))
>>>>>>> remotes/origin/feature/ph1.3:web/web-front/ipdds/ipdds_app/views/view_10401_compare.py
        return JsonResponse(dto, safe=False)