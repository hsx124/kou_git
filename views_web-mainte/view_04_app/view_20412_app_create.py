import json
from django.shortcuts import render, redirect
from django.db import transaction

from admin_app.views.view_main import MainView
from admin_app.service.service_04_app.service_20412_app_create import AppCreateService

class AppCreateView(MainView):

    # サービスクラス
    appCreateService = AppCreateService()

    # テンプレート
    template_name = 'admin_app/04_app/20412_app_create.html'

    def get(self, request):
        '''
        初期表示処理
        '''
        context = {}
        ipcode = ''

        if 'ipc' in request.GET:
            ipcode = request.GET['ipc']
        # サービスの実行
        dto = self.appCreateService.bizProcess(ipcode)

        # javascriptデータ連携用
        #context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        '''
        保存ボタン、保存してもう一つ追加ボタン押下時
        '''
        context = {}
        appname= ''
        if 'app_name' in request.GET:
            appname = request.GET['app_name']

        #サービスの実行
        dto = self.appCreateService.createMMobileApp(request, appname)
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # エラーがない場合、且つ、「保存してもう一つ追加」ボタン押下の場合、
        # 「アプリマスタ 新規登録画面」へリダイレクト
        if 'save_more_one' in request.POST:
            response = redirect('admin_app:20412_app_create')
            get_params = request.GET.urlencode()
            response['location'] += '?'+get_params
            return response

        # エラーがない場合、且つ、保存ボタンを押下の場合、
        # 「アプリマスタ 一覧画面」へリダイレクト
        response = redirect('admin_app:20411_app_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('app_name'),
            'status' : 'create'
        }

        return response
