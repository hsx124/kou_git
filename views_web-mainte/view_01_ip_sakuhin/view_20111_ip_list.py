import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView
from admin_app.service.service_01_ip_sakuhin.service_20111_ip_list import IpListService


class IpListView(ListView):

    #サービスクラス
    ipListService = IpListService()
    #テンプレート
    template_name = 'admin_app/01_ip_sakuhin/20111_ip_list.html'

    def get(self, request):
        """GET処理"""
        if request.is_ajax():
            # 非同期処理実行
            return self.ajax(request)
        else:
            # 初期表示処理
            return self.init(request)
    
    def init(self, request):
        """初期表示処理"""
        context = {}
        # サービスの実行
        dto = self.ipListService.initialize('m_ip')

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)

    def ajax(self, request):
        """非同期処理(IP一覧データ取得)"""
        dto = {}
        # サービスの実行
        # IP一覧検索時
        if 'ip' in request.GET:
            dto = self.ipListService.getIpList()
        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    # ポスト通信（削除処理）
    def post(self, request):

        # IPコード・IP名を取得
        ip_code = request.POST.get('delete-ip-code')
        ip_name = request.POST.get('delete-ip-name')

        # 更新ユーザの姓名取得
        full_name = request.user.get_full_name()

        #サービスの実行
        dto = self.ipListService.deleteIpData(ip_code, ip_name, full_name)

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    def csvdownload(request):
        ipListService = IpListService()
        # CSVダウンロード（全件）
        response = HttpResponse(content_type='text/csv')
        filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        csv_date = ipListService.getIpCsvData()

        #csv書き込み
        writer = csv.writer(response)

        # ヘッダー出力
        header = [
            'IPコード',
            'IP名',
            'IPかな名',
            'IP管理フラグ',
            '作成者',
            '作成日時',
            '最終更新者',
            '最終更新日時']
        writer.writerow(header)

        # IP情報書き出し
        for row in csv_date:
            # 日付を-区切り→/区切りに変換 ex)2019-01-12→2019→2019/01/12
            keys = ['create_time', 'update_time']
            for key in keys:
                row[key] = ListView.csvDateFormat(row[key])

            # 表示フラグ（True->False）を(IPで管理する/IPで管理しない)に変換　ex)True->表示
            if row['ip_control_flg']:
                row['ip_control_flg'] = 'IPで管理する'
            else:
                row['ip_control_flg'] = 'IPで管理しない'

            row_list = list(row.values())
            writer.writerow(row_list)

        return response

