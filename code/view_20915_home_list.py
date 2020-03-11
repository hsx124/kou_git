import json
import urllib
import csv
from django.http.response import HttpResponse
from django.shortcuts import redirect,render
from django.http.response import JsonResponse
from admin_app.views.view_list import ListView

from admin_app.service.service_09_home.service_20915_home_list import HomeListService

from django.db import transaction

import urllib.parse

class HomeListView(ListView):
    
    #サービスクラス
    homeListService = HomeListService()

    #テンプレート
    template_name = 'admin_app/09_home/20915_home_list.html'
    
    def get(self, request):

        context = {}

        #サービスの実行:サービスの業務プロセス呼ぶ
        dto = self.homeListService.initialize('t_top_news','m_banner')
        
        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)

        # 組み込みタグ用
        context['object_to_html'] = dto
        
        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self,request):
        
        context ={}
        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        # 更新ボタン
        if 'news_update' in request.POST:
            context = self.homeListService.homeListProcess(request,request.POST['news_id'])
            if context['is_error']:
                json.dumps(context, default=self.json_serial)
                return JsonResponse(context, safe=False)
        # 新規ボタン
        elif 'news_create' in request.POST:
            context = self.homeListService.homeListCreateProcess(request,request.POST['news_id'])
            if context['is_error']:
                json.dumps(context, default=self.json_serial)
                return JsonResponse(context, safe=False)
        # バナー表示/非表示切替
        if 'banner-disable' in request.POST:
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            self.homeListService.homeBannerProcess(request.POST['banner-disable'],full_name)
        return JsonResponse(context, safe=False)

    def changecsvdownload(request):
        '''
        変更履歴CSVダウンロード
        '''
        response = HttpResponse(content_type='text/csv')
        filename = urllib.parse.quote(('CSVファイル.csv').encode("utf8"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        if 'date-start' in request.GET:
            csv_date = HomeListService.changeCsvDownloadProcess(HomeListService, request.GET.get('table-name'),request.GET.get('table-name2'), request.GET.get('date-start'),request.GET.get('date-end'))
        else:
            csv_date = HomeListService.changeCsvDownloadProcess(HomeListService, request.GET.get('table-name'),request.GET.get('table-name2'))

        #csv書き込み
        writer = csv.writer(response)

        # ヘッダー出力
        header = ['更新日時', '更新者', '変更マスタ', '変更対象', '操作内容', '備考']
        writer.writerow(header)
        for row in csv_date:
            writer.writerow(row)

        return response