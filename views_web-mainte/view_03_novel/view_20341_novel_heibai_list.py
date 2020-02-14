import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView
from admin_app.service.service_03_novel.service_20341_novel_heibai_list import NovelHeibaiListService


class NovelHeibaiListView(ListView):

    #サービスクラス
    novelHeibaiListService = NovelHeibaiListService()
    #テンプレート
    template_name = 'admin_app/03_novel/20341_novel_heibai_list.html'

    def init(self, request):
        '''
        初期表示処理
        '''
        context = {}
        # サービスの実行
        dto = self.novelHeibaiListService.initialize('m_heibai(novel)')

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)

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

    # ポスト通信（削除処理）
    def post(self, request):
        # 小説タイトルコード・小説タイトル名を取得
        novel_title_code = request.POST.get('delete-novel-code')
        novel_title_name = request.POST.get('delete-novel-name')

        # 更新ユーザの姓名取得
        full_name = request.user.get_full_name()

        #サービスの実行
        dto = self.novelHeibaiListService.deleteNovelHeibaiData(novel_title_code, novel_title_name, full_name)

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    def ajax(self, request):
        '''
        非同期処理(併売一覧データ取得)
        '''
        dto = {}
        # サービスの実行
        # 併売情報一覧検索時
        if 'heibai' in request.GET:
            dto = self.novelHeibaiListService.getNovelHeibaiList()

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    def csvdownload(request):
        #サービスクラス
        novelHeibaiListService = NovelHeibaiListService()

        # CSVダウンロード（全件）
        response = HttpResponse(content_type='text/csv')
        filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        csv_data = novelHeibaiListService.getNovelHeibaiCsvData()

        #csv書き込み
        writer = csv.writer(response)

        # ヘッダー出力
        header = [
            '小説タイトルコード',
            '小説タイトル名',
            '併売コード',
            '併売名1',
            '併売1',
            '併売名2',
            '併売2',
            '併売名3',
            '併売3',
            '併売名4',
            '併売4',
            '併売名5',
            '併売5',
            '作成者',
            '作成日時',
            '最終更新者',
            '最終更新日時']
        writer.writerow(header)

        # 併売情報書き出し
        for row in csv_data:
            # 日付を-区切り→/区切りに変換 ex)2019-01-12→2019→2019/01/12
            keys = ['create_time', 'update_time']
            for key in keys:
                row[key] = ListView.csvDateFormat(row[key])

            row_list = list(row.values())
            writer.writerow(row_list)

        return response

