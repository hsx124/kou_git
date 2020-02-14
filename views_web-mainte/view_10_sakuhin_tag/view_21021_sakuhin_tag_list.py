import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView
from admin_app.service.service_10_sakuhin_tag.service_21021_sakuhin_tag_list import SakuhinTagListService


class SakuhinTagListView(ListView):

    #サービスクラス
    sakuhinTagListService = SakuhinTagListService()
    #テンプレート
    template_name = 'admin_app/10_sakuhin_tag/21021_sakuhin_tag_list.html'

    def get(self, request):
        '''
        GET処理
        '''
        if request.is_ajax():
            # 非同期処理実行
            return self.ajax(request)
        else:
            # 初期表示処理
            return self.init(request)
    
    def init(self, request):
        '''
        初期表示処理
        '''
        context = {}

        # サービスの実行
        dto = self.sakuhinTagListService.initialize('m_sakuhin_tag')
        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)

        # 組み込みタグ用
        context['object_to_html'] = dto

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)

    def ajax(self, request):
        '''
        非同期処理(タグマスタ一覧データ取得)
        '''
        dto = {}
        # サービスの実行
        # タグマスタ一覧検索時
        if 'search-category-code' in request.GET:
            dto = self.sakuhinTagListService.getSakuhinTagList(request.GET.get('search-category-code'))

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)


    # ポスト通信（削除処理）
    def post(self, request):

        # 作品タグコード・作品タグ名を取得
        tag_code = request.POST.get('delete-tag-code')
        tag_name = request.POST.get('delete-tag-name')
        search_category_code = request.POST.get('search-category-code')

        # 更新ユーザの姓名取得
        full_name = request.user.get_full_name()
        
        #サービスの実行
        dto = self.sakuhinTagListService.deleteTagData(tag_code, tag_name, full_name,search_category_code)

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)


    def csvdownload(request):
        # CSVダウンロード（全件）
        sakuhinTagListService = SakuhinTagListService()

        response = HttpResponse(content_type='text/csv')
        filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        csv_date = sakuhinTagListService.getTagCsvData()

        #csv書き込み
        writer = csv.writer(response)

        # ヘッダー出力
        header = [
            'タグコード',
            'タグカテゴリ名',
            'タグ名',
            '作成者',
            '作成日時',
            '最終更新者',
            '最終更新日時']

        writer.writerow(header)

        # 作品情報書き出し
        for row in csv_date:
            # 日付を-区切り→/区切りに変換 ex)2019-01-12→2019→2019/01/12
            keys = ['create_time', 'update_time']
            for key in keys:
                row[key] = ListView.csvDateFormat(row[key])

            row_list = list(row.values())
            writer.writerow(row_list)

        return response
