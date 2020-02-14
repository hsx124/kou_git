import json
from typing import NamedTuple
from django.db import transaction
from django.shortcuts import render, redirect
from admin_app.views.view_main import MainView
from admin_app.service.service_01_ip_sakuhin.service_20113_ip_update import IpUpdateService

class IpUpdateView(MainView):

    # サービスクラス
    ipUpdateService = IpUpdateService()
    # テンプレート
    template_name = 'admin_app/01_ip_sakuhin/20113_ip_update.html'

    # 初期表示処理
    def get(self, request):

        context = {}
        ip_code = ''

        # パラメータ名が正しい場合
        if 'ipc' in request.GET:
            ip_code = request.GET['ipc']
            # サービスの実行
            dto = self.ipUpdateService.initialize(ip_code)

            # 編集対象存在しない場合、一覧画面に戻る
            if dto['value_not_found']:
                # IPコード存在しないる場合
                # 「IP情報一覧画面」へリダイレクト
                response = redirect('admin_app:20111_ip_list')

                # セッションを保存
                request.session['show_msg'] = {
                    'targetname' : 'IP情報',
                    'status' : 'value_error'}
                return response
            else:
                # 編集対象存在する場合、編集画面へ遷移する
                # javascriptデータ連携用
                context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
                # 組み込みタグ用
                context['object_to_html'] = dto
                return render(request, self.template_name, context)
        else:
            # パラメータ名が不正な場合
            # 「IP一覧画面」へリダイレクト
            response = redirect('admin_app:20111_ip_list')
            # セッションを保存
            request.session['show_msg'] = {'status' : 'param_error'}

            return response

    # 保存ボタン
    @transaction.atomic
    def post(self, request):
        context ={}

        #サービスの実行
        dto = self.ipUpdateService.updateIpData(request)
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        else:
            # エラーがない場合、且つ、保存ボタンを押下の場合、
            # 「IP情報一覧画面」へリダイレクト
            response = redirect('admin_app:20111_ip_list')

            # セッションを保存
            request.session['show_msg'] = {
                'targetname' : request.POST.get('ip_name'),
                'status' : 'update'
            }

        return response

