import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView
from admin_app.service.service_01_ip_sakuhin.service_20121_sakuhin_list import SakuhinListService

class SakuhinListView(ListView):

    #サービスクラス
    sakuhinListService = SakuhinListService()
    #テンプレート
    template_name = 'admin_app/01_ip_sakuhin/20121_sakuhin_list.html'

    def get(self,request) :
        """AjaxのGet処理"""
        if request.is_ajax():
            return self.ajax(request)
        else:
            return self.init(request)

    def init(self, request):
        """初期処理"""
        context = {}

        # サービスの実行
        dto = self.sakuhinListService.initialize('m_sakuhin')

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)

        # 組み込みタグ用
        context['object_to_html'] = dto

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)

    def ajax(self,request):
        """非同期処理(作品一覧データ取得)"""
        dto = {}
        # サービスの実行
        # 作品一覧検索時
        if 'sakuhin-list' in request.GET:
            dto = self.sakuhinListService.getSakuhinList()
        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)
    # ポスト通信
    def post(self, request):

        sakuhinCode = request.POST.get('delete-sakuhincode')
        sakuhinName = request.POST.get('delete-sakuhinname')

        # ユーザの姓名取得
        full_name = request.user.get_full_name()
        #サービスの実行
        dto = self.sakuhinListService.deleteSakuhinData(sakuhinCode,sakuhinName,full_name)

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    def csvdownload(request):
        sakuhinListService = SakuhinListService()
        # CSVダウンロード（全件）

        response = HttpResponse(content_type='text/csv')
        filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        csv_date = sakuhinListService.getSakuhinCsvData()

        #csv書き込み
        writer = csv.writer(response)

        # ヘッダー出力
        header = [
            '作品コード',
            '作品名',
            '作品かな名',
            'キービジュアルファイル名',
            '発表年月',
            '作品公開有効期間_開始年月日',
            '作品公開有効期間_終了年月日',
            '国外窓口',
            '国内窓口',
            'メモ',
            '作品概要',
            'キーワード',
            '無効フラグ',
            '作成者',
            '作成日時',
            '更新者',
            '更新日時']
        writer.writerow(header)

        # 作品情報書き出し
        for row in csv_date:

            # htmlタグ除去
            if row['overview'] != None:
                row['overview'] = re.sub('<("[^"]*"|\'[^\']*\'|[^\'">])*>', '', row['overview'])

            # 改行コードを文字列に置換
            keys = ['memo', 'domestic_window', 'foreign_window', 'overview']
            for key in keys:
                if row[key] != None:
                    row[key] = re.sub('\r\n|\n|\r', '(改行)', row[key])

            # 日付を-区切り→/区切りに変換 ex)2019-01-12→2019→2019/01/12
            keys = ['release_yyyymm','valid_start_yyyymmdd','valid_end_yyyymmdd','create_time', 'update_time']
            for key in keys:
                row[key] = ListView.csvDateFormat(row[key])

            row_list = list(row.values())
            writer.writerow(row_list)

        return response
