import json
from django.db import transaction
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.service.service_03_novel.service_20312_novel_create import NovelCreateService

class NovelCreateView(MainView):

    #サービスクラス
    novelCreateService = NovelCreateService()
    #テンプレート
    template_name = 'admin_app/03_novel/20312_novel_create.html'

    # 初期表示時
    def init(self,request):

        # コンテキストの取得
        context = {}
        #サービスの実行
        dto = self.novelCreateService.initialize()

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)

    # 保存ボタン、保存してもう一つ追加ボタン
    @transaction.atomic
    def post(self, request):

        context ={}
        #サービスの実行
        dto = self.novelCreateService.createNovelData(request)
        # javascriptデータ連携用
        context['object_to_javascript'] = json.dumps(dto, default=self.json_serial)
        #組み込みタグ用
        context['object_to_html'] = dto

        # エラーがある場合はエラー情報とユーザ入力情報をもとに再入力を促す。
        if dto['is_error']:
            return render(request, self.template_name, context)

        # エラーがない場合、且つ、「保存してもう一つ追加」ボタン押下の場合、
        # 「小説情報 新規登録画面」へリダイレクト
        if 'save_more_one' in request.POST:
            return redirect('admin_app:20312_novel_create')

        # エラーがない場合、且つ、保存ボタンを押下の場合、
        # 「小説一覧画面」へリダイレクト
        response = redirect('admin_app:20311_novel_list')

        # セッションを保存
        request.session['show_msg'] = {
            'targetname' : request.POST.get('novel_title_name'),
            'status' : 'create'
        }

        return response

    def get(self, request):
        '''
        GET処理
        '''
        if request.is_ajax():
            # 非同期処理実行
            return self.ajax(request)
        else:
            return self.init(request)

    def ajax(self,request):
        process_code = request.GET.get('process_code')
        # サービスの実行
        if 'media' == process_code:
            # 掲載媒体取得
            dto = self.novelCreateService.searchMedia(request.GET.get('keyword'))
        elif 'publisher' == process_code:
            # 出版社取得
            dto = self.novelCreateService.searchPublisher(request.GET.get('keyword'))
        elif 'staff_role' == process_code:
            # スタッフ役割取得
            dto = self.novelCreateService.searchStaffRole(request.GET.get('keyword'))
        elif 'staff' == process_code:
            # スタッフ役割取得
            dto = self.novelCreateService.searchStaff(request.GET.get('keyword'))

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)
