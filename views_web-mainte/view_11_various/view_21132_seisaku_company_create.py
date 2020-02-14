import json
import urllib.parse

from django.shortcuts import render, redirect
from django.db import transaction
from admin_app.views.view_main import MainView
from admin_app.service.service_11_various.service_21132_seisaku_company_create import SeisakuCompanyCreateService

class SeisakuCompanyCreateView(MainView):

    #サービスクラス
    seisakucompanyCreateService = SeisakuCompanyCreateService()
    #テンプレート
    template_name = 'admin_app/11_various/21132_seisaku_company_create.html'
    

    # 初期表示時
    def get_context_data(self, **kwargs):

        # コンテキストの取得
        context = super().get_context_data(**kwargs)
        #サービスの実行
        dto = self.seisakucompanyCreateService.initialize()

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        return context 
    
    # 保存ボタン、保存してもう一つ追加ボタン
    @transaction.atomic
    def post(self, request):

        context ={}
        #サービスの実行
        dto = self.seisakucompanyCreateService.createSeisakuCompanyData(request)
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # エラーがない場合、且つ、「保存してもう一つ追加」ボタン押下の場合、
        # 「制作会社マスタ 新規登録画面」へリダイレクト
        if 'save_more_one' in request.POST:
            return redirect('admin_app:21132_seisaku_company_create')

        # エラーがない場合、且つ、保存ボタンを押下の場合、
        # 「制作会社一覧画面」へリダイレクト
        response = redirect('admin_app:21131_seisaku_company_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('seisaku_company_name'),
            'status' : 'create'
        }

        return response

