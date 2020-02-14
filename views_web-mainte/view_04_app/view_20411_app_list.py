import csv
import json
import urllib

from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponse

from admin_app.views.view_list import ListView
from admin_app.service.service_04_app.service_20411_app_list import AppListService

class AppListView(ListView):

    #サービスクラス
    appListService = AppListService()

    #テンプレート
    template_name = 'admin_app/04_app/20411_app_list.html'

    def get(self, request):
        '''
        GET処理
        '''

        if request.is_ajax():
            # 非同期処理
            return self.ajax(request)
        else:
            # 初期描画
            return self.initialize(request)


    def post(self, request):
        '''
        POST処理
        '''

        dto = {}

        # ユーザの姓名取得
        full_name = request.user.get_full_name()

        # サービスの実行
        # 書籍削除時処理
        if 'delete-app' in request.POST:
            dto = self.appListService.deleteAppProcess(request.POST['reload-ipcode'], request.POST['delete-app'],full_name)

        return JsonResponse(dto, safe=False)

    def ajax(self, request):
        '''
        非同期処理
        '''
        dto = {}

        # サービスの実行
        # IPコード検索時
        if 'input-ipcode' in request.GET:
            dto = self.appListService.ipcodeSearchProcess(request.GET['input-ipcode'])

        # IP名検索時
        elif 'input-ipname' in request.GET:
            dto = self.appListService.ipnameSearchProcess(request.GET['input-ipname'])

        # IP選択（グリッド描画）時
        elif 'ip-list' in request.GET:
            dto = self.appListService.getGridDataProcess(request.GET.get('ip-list'))

        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    def initialize(self, request):
        # 同期処理
        #サービスの実行
        context = {}
        dto = {}

        dto = self.appListService.bizProcess('m_mobile_app')
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)

    def csvdownload(request):
        # CSVダウンロード（全件/IP毎）

        response = HttpResponse(content_type='text/csv')
        filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        if 'ip-list' in request.GET:
            csv_date = AppListService.getCsvDataProcess(AppListService, request.GET.get('ip-list'))
        else:
            csv_date = AppListService.getCsvDataProcess(AppListService)

        #csv書き込み
        writer = csv.writer(response)

        # ヘッダー出力
        header = ['アプリ名','アプリID_Android','アプリID_iOS','販売元','サービス開始年月日','サービス終了年月日','作成者','作成日時','最終更新者','最終更新日時',]
        writer.writerow(header)
        for row in csv_date:
            writer.writerow(row)

        return response
