import json
from django.shortcuts import render, redirect
from django.db import transaction

from admin_app.views.view_main import MainView
from admin_app.service.service_04_app.service_20413_app_update import AppUpdateService

class AppUpdateView(MainView):

    # サービスクラス
    appUpdateService = AppUpdateService()

    # テンプレート
    template_name = 'admin_app/04_app/20413_app_update.html'

    def get(self, request):
        '''
        初期表示処理
        '''
        context = {}
        ipcode = ''
        appname = ''

        if ('ipc' in request.GET
            and 'app_name' in request.GET):
            ipcode = request.GET['ipc']
            appname = request.GET['app_name']
            
        # サービスの実行
        dto = self.appUpdateService.bizProcess(ipcode, appname)

        # javascriptデータ連携用
        #context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        '''
        保存ボタン押下時
        '''

        context = {}
        ipcode = ''
        appname = ''

        if ('ipc' in request.GET
            and 'app_name' in request.GET):
            ipcode = request.GET['ipc']
            appname = request.GET['app_name']

        #サービスの実行
        dto = self.appUpdateService.updateMMobileApp(request, ipcode, appname)
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # エラーがない場合、且つ、保存ボタンを押下の場合、
        # 「アプリマスタ 一覧画面」へリダイレクト
        response = redirect('admin_app:20411_app_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('app_name'),
            'status' : 'update'
        }

        return response
