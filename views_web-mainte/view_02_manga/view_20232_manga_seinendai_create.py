import csv
import json
import urllib
from django.db import transaction
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_list import ListView
# from admin_app.service.service_02_manga.service_20222_manga_create import MangaCreateService


class MangaSeinendaiCreateView(ListView):

    #サービスクラス
    #mangaSeinendaiCreateService = MangaCreateService()
    #テンプレート
    template_name = 'admin_app/02_manga/20232_manga_seinendai_create.html'

    def get(self, request):
        '''
        GET処理
        '''

        if request.is_ajax():
            # 非同期処理実行
            return self.ajax(request)
        else:
            # 初期表示処理
            return self.initialize(request)

    # 保存ボタン、保存してもう一つ追加ボタン
    @transaction.atomic
    def post(self, request):
        '''
        POST処理（書籍新規登録）
        '''

        context ={}

        #サービスの実行
        ipcode = ''
        #if 'ipc' in request.GET:
        #    ipcode = request.GET['ipc']

        #dto = self.mangaCreateService.createMBook(request, ipcode)

        # javascriptデータ連携用
        #context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        #context['object_to_html'] = dto
        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # エラーがない場合、且つ、「保存してもう一つ追加」ボタン押下の場合、
        # 「書籍マスタ 新規登録画面」へリダイレクト
        if 'save_more_one' in request.POST:
            response = redirect('admin_app:20222_manga_create')
            get_params = request.GET.urlencode()
            response['location'] += '?'+get_params
            return response

        # エラーがない場合、且つ、保存ボタンを押下の場合、
        # 「書籍マスタ一覧画面」へリダイレクト
        response = redirect('admin_app:20221_manga_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('book_name'),
            'status' : 'create'
        }
        return response

    def ajax(self, request):
        '''
        非同期処理
        書籍名からISBN取得
        '''
        dto = {}

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    def initialize(self, request):
        '''
        初期表示処理
        '''
        context = {}

        ipcode = ''
        if 'mangac' in request.GET:
            ipcode = request.GET['mangac']

        dto = {}
        # サービスの実行
        #dto = self.mangaCreateService.initialize(ipcode)

        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        return render(request, self.template_name, context) 
