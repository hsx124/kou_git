import csv
import json
import urllib

from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponse

from admin_app.views.view_list import ListView
from admin_app.service.service_05_anime.service_20511_anime_list import AnimeListService


class AnimeListView(ListView):

    #サービスクラス
    animeListService = AnimeListService()

    #テンプレート
    template_name = 'admin_app/05_anime/20511_anime_list.html'

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
        # アニメ削除時処理
        if 'delete-anime-name' in request.POST:
            dto = self.animeListService.deleteAnimeProcess(request.POST['reload-sakuhin-code'], request.POST['delete-anime-name'],full_name)

        return JsonResponse(dto, safe=False)

    def ajax(self, request):
        '''
        非同期処理
        '''
        dto = {}

        # サービスの実行
        # 作品コード検索時
        if 'input-sakuhin-code' in request.GET:
            dto = self.animeListService.sakuhinCodeSearchProcess(request.GET['input-sakuhin-code'])
        # 作品名検索時
        elif 'input-sakuhin-name' in request.GET:
            dto = self.animeListService.sakuhinNameSearchProcess(request.GET['input-sakuhin-name'])
        # 作品選択（グリッド描画）時
        elif 'sakuhin-list' in request.GET:
            dto = self.animeListService.getGridDataProcess(request.GET.get('sakuhin-list'))
            print(dto)

        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    def initialize(self, request):
        # 同期処理
        # サービスの実行
        context = {}
        dto = {}

        dto = self.animeListService.bizProcess('m_anime_title')
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)

    def csvdownload(request):
        # CSVダウンロード（全件）

        response = HttpResponse(content_type='text/csv')
        filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        csv_date = AnimeListService.getCsvDataProcess(AnimeListService)

        #csv書き込み
        writer = csv.writer(response)

        # ヘッダー出力
        header = ['作品コード','TV番組名','放送局','放送期間','作成者','作成日時','最終更新者','最終更新日時',]
        writer.writerow(header)
        for row in csv_date:
            writer.writerow(row)

        return response
