import json
from django.db import transaction
from django.shortcuts import render, redirect

from admin_app.views.view_main import MainView
from admin_app.service.service_02_manga.service_20213_manga_update import MangaUpdateService

class MangaUpdateView(MainView):

    #サービスクラス
    mangaUpdateService = MangaUpdateService()
    #テンプレート
    template_name = 'admin_app/02_manga/20213_manga_update.html'

        # 初期表示処理
    def get(self, request):

        context = {}
        manga_title_code = ''

        # パラメータ名が正しい場合
        if 'mangac' in request.GET:
            manga_title_code = request.GET['mangac']

            # サービスの実行
            dto = self.mangaUpdateService.initialize(manga_title_code)

            # 編集対象存在しない場合、一覧画面に戻る
            if dto['value_not_found']:
                # マンガタイトルコードが存在しない場合
                # 「マンガ情報一覧画面」へリダイレクト
                response = redirect('admin_app:20211_manga_list')

                # セッションを保存
                request.session['show_msg'] = {
                    'targetname' : 'マンガ情報',
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
            # 「マンガ情報一覧画面」へリダイレクト
            response = redirect('admin_app:20211_manga_list')
            # セッションを保存
            request.session['show_msg'] = {'status' : 'param_error'}

            return response


    # 保存ボタン
    @transaction.atomic
    def post(self, request):

        context ={}

        #サービスの実行
        dto = self.mangaUpdateService.updateMangaData(request)

        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        else:
            # エラーがない場合、且つ、保存ボタンを押下の場合、
            # 「マンガ情報一覧画面」へリダイレクト
            response = redirect('admin_app:20211_manga_list')

            # セッションを保存
            request.session['show_msg'] = {
                'targetname' : request.POST.get('manga_title_name'),
                'status' : 'update'
            }

        return response
