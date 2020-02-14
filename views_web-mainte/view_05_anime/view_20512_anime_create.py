import json
from django.shortcuts import render, redirect
from django.db import transaction

from admin_app.views.view_main import MainView
from admin_app.service.service_05_anime.service_20512_anime_create import AnimeCreateService

class AnimeCreateView(MainView):

    # サービスクラス
    animeCreateService = AnimeCreateService()

    # テンプレート
    template_name = 'admin_app/05_anime/20512_anime_create.html'

    def get(self, request):
        '''
        初期表示処理
        '''
        context = {}
        ipcode = ''

        if 'ipc' in request.GET:
            ipcode = request.GET['ipc']

        # サービスの実行
        dto = self.animeCreateService.bizProcess(ipcode)

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
        dto = self.animeCreateService.createMWiki(request)

        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # エラーがない場合、且つ、「保存してもう一つ追加」ボタン押下の場合、
        # 「アニメマスタ 新規登録画面」へリダイレクト
        if 'save_more_one' in request.POST:
            response = redirect('admin_app:20512_anime_create')
            get_params = request.GET.urlencode()
            response['location'] += '?'+get_params
            return response

        # エラーがない場合、且つ、保存ボタンを押下の場合、
        # 「アニメマスタ 一覧画面」へリダイレクト
        response = redirect('admin_app:20511_anime_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('tv_program_name'),
            'status' : 'create'
        }

        return response
