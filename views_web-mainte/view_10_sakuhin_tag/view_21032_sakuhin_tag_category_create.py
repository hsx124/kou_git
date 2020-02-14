import json
from django.db import transaction
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.service.service_10_sakuhin_tag.service_21032_sakuhin_tag_category_create import SakuhinTagCategoryCreateService

class SakuhinTagCategoryCreateView(MainView):

    #サービスクラス
    sakuhinTagCategoryCreateService = SakuhinTagCategoryCreateService()
    #テンプレート
    template_name = 'admin_app/10_sakuhin_tag/21032_sakuhin_tag_category_create.html'

    # 初期表示時
    def init(self,request):

        # コンテキストの取得
        context = {}
        #サービスの実行
        dto = self.sakuhinTagCategoryCreateService.initialize()

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)

    # 初期表示時
    def get_context_data(self, **kwargs):

        # コンテキストの取得
        context = super().get_context_data(**kwargs)
        #サービスの実行
        dto = self.sakuhinTagCategoryCreateService.initialize()

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
        dto = self.sakuhinTagCategoryCreateService.createSakuhinTagCategoryData(request)
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # エラーがない場合、且つ、「保存してもう一つ追加」ボタン押下の場合、
        # 「タグカテゴリ情報 新規登録画面」へリダイレクト
        if 'save_more_one' in request.POST:
            return redirect('admin_app:21032_sakuhin_tag_category_create')

        # エラーがない場合、且つ、保存ボタンを押下の場合、
        # 「タグカテゴリ情報一覧画面」へリダイレクト
        response = redirect('admin_app:21031_sakuhin_tag_category_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('sakuhin_tag_category_name'),
            'status' : 'create'
        }

        return response

