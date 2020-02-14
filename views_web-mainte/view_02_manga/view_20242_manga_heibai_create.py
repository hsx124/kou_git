import json
from django.db import transaction
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.service.service_02_manga.service_20242_manga_heibai_create import MangaHeibaiCreateService

class MangaHeibaiCreateView(MainView):

    #サービスクラス
    mangaHeibaiCreateService = MangaHeibaiCreateService()
    #テンプレート
    template_name = 'admin_app/02_manga/20242_manga_heibai_create.html'

    # 初期表示時
    def init(self,request):

        # コンテキストの取得
        context = {}
        manga_title_code = ''

        # パラメータ名が正しい場合
        if 'mangac' in request.GET:
            manga_title_code = request.GET['mangac']

            # サービスの実行
            dto = self.mangaHeibaiCreateService.initialize(manga_title_code)
            # 編集対象存在しない場合、一覧画面に戻る
            if dto['value_not_found']:
                # マンガタイトルコードが存在しない場合
                # 「併売情報一覧画面」へリダイレクト
                response = redirect('admin_app:20241_manga_heibai_list')

                # セッションを保存
                request.session['show_msg'] = {
                    'targetname' : '併売情報',
                    'status' : 'value_error'}
                return response
            else:
                # 編集対象が存在する場合、編集画面へ遷移する
                # javascriptデータ連携用
                context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
                # 組み込みタグ用
                context['object_to_html'] = dto

                return render(request, self.template_name, context)
        else:
            # パラメータ名が不正な場合
            # 「併売情報一覧画面」へリダイレクト
            response = redirect('admin_app:20241_manga_heibai_list')
            # セッションを保存
            request.session['show_msg'] = {'status' : 'param_error'}

            return response

    # 保存ボタン、保存してもう一つ追加ボタン
    @transaction.atomic
    def post(self, request):

        context ={}
        #サービスの実行
        dto = self.mangaHeibaiCreateService.createMangaHeibaiData(request)
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # エラーがない場合、且つ、「保存してもう一つ追加」ボタン押下の場合、
        # 「併売情報 新規登録画面」へリダイレクト
        if 'save_more_one' in request.POST:
            return redirect('admin_app:20242_manga_heibai_create')

        # エラーがない場合、且つ、保存ボタンを押下の場合、
        # 「併売一覧画面」へリダイレクト
        response = redirect('admin_app:20241_manga_heibai_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('manga_title_name'),
            'status' : 'create'
        }

        return response

    def get(self, request):
        '''
        GET処理
        '''
        if request.is_ajax():
            # 非同期処理実行
            return self.ajax(request)
        else:
            return self.init(request)

    def ajax(self,request):
        # サービスの実行
        dto = self.mangaHeibaiCreateService.getSakuhinByTitleName(request.GET.get('keyword'))

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)
