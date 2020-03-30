import json
from typing import NamedTuple
from django.db import transaction
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from admin_app.views.view_main import MainView
from admin_app.service.service_07_twitter.service_20713_twitter_update import TwitterUpdateService

class TwitterUpdateView(MainView):

    # サービスクラス
    twitterUpdateService = TwitterUpdateService()
    # テンプレート
    template_name = 'admin_app/07_twitter/20713_twitter_update.html'

    # 初期表示処理
    def get(self, request):

        context = {}
        twitter_code = ''

        # パラメータ名が正しい場合
        if 'twitterc' in request.GET:
            twitter_code = request.GET['twitterc']

            # サービスの実行
            dto = self.twitterUpdateService.initialize(twitter_code)

            # 編集対象存在しない場合、一覧画面に戻る
            if dto['value_not_found']:
                # Twitterコード存在しないる場合
                # 「Twitter一覧画面」へリダイレクト
                response = redirect('admin_app:20711_twitter_list')

                # セッションを保存
                request.session['show_msg'] = {
                    'targetname' : 'Twitterアカウント',
                    'status' : 'value_error'}
                return response
            else:
                # 編集対象存在する場合、編集画面へ遷移する
                # javascriptデータ連携用
                context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
                # 組み込みタグ用
                context['object_to_html'] = dto

                return render(request, self.template_name, context)

        elif 'change' in request.GET:
            twitter_code = request.GET['change']
            param={
                'twitter_code':twitter_code
            }
            dto = self.twitterUpdateService.changeMainFlg(param)
            return JsonResponse(dto, safe=False)
        else:
            # パラメータ名が不正な場合
            # 「Twitter一覧画面」へリダイレクト
            response = redirect('admin_app:20711_twitter_list')
            # セッションを保存
            request.session['show_msg'] = {'status' : 'param_error'}

            return response


    # 保存ボタン
    @transaction.atomic
    def post(self, request):

        context ={}

        if 'unlock-twitter-code' in request.POST:
            sakuhin_map_id = request.POST.get('sakuhin_map_id')
            account_name = request.POST.get('unlock-account-name')
            full_name = request.user.get_full_name()
            param={
                'sakuhin_map_id':sakuhin_map_id,
                'full_name':full_name,
                'account_name':account_name
            }
            dto = self.twitterUpdateService.deleteMapData(param)
            # 非同期処理
            json.dumps(dto, default=self.json_serial)
            return JsonResponse(dto, safe=False)

        #サービスの実行
        dto = self.twitterUpdateService.updateTwitterData(request)
        
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        else:
            # エラーがない場合、且つ、保存ボタンを押下の場合、
            # 「Twitter一覧画面」へリダイレクト
            response = redirect('admin_app:20711_twitter_list')

            # セッションを保存
            request.session['show_msg'] = {
                'targetname' : request.POST.get('account_name'),
                'status' : 'update'
            }

        return response
