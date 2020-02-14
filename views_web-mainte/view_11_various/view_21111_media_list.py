import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView
from admin_app.service.service_11_various.service_21111_media_list import MediaListService


class MediaListView(ListView):

    #サービスクラス
    mediaListService = MediaListService()
    #テンプレート
    template_name = 'admin_app/11_various/21111_media_list.html'

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
        dto = self.mediaListService.initialize('m_media')

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
        非同期処理(掲載媒体一覧データ取得)
        '''
        dto = {}
        # サービスの実行
        # 掲載媒体一覧検索時
        if 'media' in request.GET:
            dto = self.mediaListService.getMediaList()

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    # ポスト通信（削除処理を行い）
    def post(self, request):
    
        # 掲載媒体コード・掲載媒体名を取得
        media_code = request.POST.get('delete-media-code')
        media_name = request.POST.get('delete-media-name')

        # 更新ユーザの姓名取得
        full_name = request.user.get_full_name()

        #サービスの実行
        dto = self.mediaListService.deleteMediaData(media_code, media_name, full_name)

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    def csvdownload(request):
        mediaListService = MediaListService()
        # CSVダウンロード（全件）
        response = HttpResponse(content_type='text/csv')
        filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        csv_data = mediaListService.getMediaCsvData()

        #csv書き込み
        writer = csv.writer(response)

        # ヘッダー出力
        header = [
            '掲載媒体コード',
            '掲載媒体名',
            '表示/非表示',
            '優先順位',
            '作成者',
            '作成日時',
            '最終更新者',
            '最終更新日時']
        writer.writerow(header)

        # 掲載媒体情報書き出し
        for row in csv_data:
            # 日付を-区切り→/区切りに変換 ex)2019-01-12→2019→2019/01/12
            keys = ['create_time', 'update_time']
            for key in keys:
                row[key] = ListView.csvDateFormat(row[key])

            # 表示フラグ（True->False）を(表示/非表示)に変換　ex)True->表示
            if row['show_flg']:
                row['show_flg'] = '表示'
            else:
                row['show_flg'] = '非表示'

            row_list = list(row.values())
            writer.writerow(row_list)

        return response
