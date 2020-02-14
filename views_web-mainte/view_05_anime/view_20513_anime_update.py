import json
from django.shortcuts import render, redirect
from django.db import transaction

from admin_app.views.view_main import MainView
from admin_app.service.service_05_anime.service_20513_anime_update import AnimeUpdateService

class AnimeUpdateView(MainView):

    # サービスクラス
    animeUpdateService = AnimeUpdateService()

    # テンプレート
    template_name = 'admin_app/05_anime/20513_anime_update.html'

    def get(self, request):
        '''
        初期表示処理
        '''
        context = {}
        ipcode = ''
        animename = ''

        if 'ipc' in request.GET:
            ipcode = request.GET['ipc']
            animename = request.GET['anime_name']

        # サービスの実行
        dto = self.animeUpdateService.bizProcess(ipcode, animename)

        # 組み込みタグ用
        context['object_to_html'] = dto

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        '''
        保存ボタン
        '''
        context = {}
        animename= ''

        if 'anime_name' in request.GET:
            animename = request.GET['anime_name']

        #サービスの実行
        dto = self.animeUpdateService.updateMWiki(request, animename)

        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # 「アニメマスタ 一覧画面」へリダイレクト
        response = redirect('admin_app:20511_anime_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('tv_program_name'),
            'status' : 'update'
        }
        print(request.session['show_msg'])
        return response