from admin_app.views.view_main import MainView
from admin_app.service.service_01_ip_sakuhin.service_20122_sakuhin_create import SakuhinCreateService
import json
from django.shortcuts import render, redirect
from django.db import transaction
import urllib.parse


class SakuhinCreateView(MainView):

    #サービスクラス
    sakuhinCreateService = SakuhinCreateService()
    #テンプレート
    template_name = 'admin_app/01_ip_sakuhin/20122_sakuhin_create.html'

    # 初期表示時
    def get_context_data(self, **kwargs):

        # コンテキストの取得
        context = super().get_context_data(**kwargs)

        #サービスの実行
        dto = self.sakuhinCreateService.bizProcess()

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        return  context
    
    # 保存ボタン、保存してもう一つ追加ボタン
    @transaction.atomic
    def post(self, request):

        context ={}
        #サービスの実行
        dto = self.sakuhinCreateService.createMIp(request)
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # エラーがない場合、且つ、「保存してもう一つ追加」ボタン押下の場合、
        # 「IPマスタ 新規登録画面」へリダイレクト
        if 'save_more_one' in request.POST:
            return redirect('admin_app:20122_sakuhin_create')

        # エラーがない場合、且つ、保存ボタンを押下の場合、
        # 「IP一覧画面」へリダイレクト
        response = redirect('admin_app:20121_sakuhin_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('ip_name'),
            'status' : 'create'
        }

        return response

