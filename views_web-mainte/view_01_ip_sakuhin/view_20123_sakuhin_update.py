import json
from typing import NamedTuple
from django.db import transaction
from django.shortcuts import render, redirect
from admin_app.views.view_main import MainView
from admin_app.service.service_01_ip_sakuhin.service_20123_sakuhin_update import SakuhinUpdateService

class SakuhinUpdateView(MainView):

    # サービスクラス
    sakuhinUpdateService = SakuhinUpdateService()
    # テンプレート
    template_name = 'admin_app/01_ip_sakuhin/20123_sakuhin_update.html'

    def get(self, request):
        '''
        初期表示処理
        '''
        context = {}

        sakuhinCode = ''
        if 'sakuhinc' in request.GET:
            sakuhinCode = request.GET['sakuhinc']
        # サービスの実行
        dto = self.sakuhinUpdateService.initialize(sakuhinCode)
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        return render(request, self.template_name, context)

    # 保存ボタン
    @transaction.atomic
    def post(self, request):
        context ={}

        #サービスの実行
        dto = self.sakuhinUpdateService.updateMIp(request)
        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        else:
            # エラーがない場合、且つ、保存ボタンを押下の場合、
            # 「IP一覧画面」へリダイレクト
            response = redirect('admin_app:20121_sakuhin_list')

            # セッションを保存
            request.session['show_msg'] = {
                'targetname' : request.POST.get('sakuhin_name'),
                'status' : 'update'
            }

        return response

