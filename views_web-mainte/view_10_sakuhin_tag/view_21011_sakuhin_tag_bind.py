import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView
from admin_app.service.service_10_sakuhin_tag.service_21011_sakuhin_tag_bind import SakuhinTagBindService


class SakuhinTagBindView(ListView):

    #サービスクラス
    sakuhinTagBindService = SakuhinTagBindService()
    #テンプレート
    template_name = 'admin_app/10_sakuhin_tag/21011_sakuhin_tag_bind.html'

    def get(self, request):
        ''' 
        GET処理
        '''
        if request.is_ajax():
            # 非同期処理実行
            return self.ajax(request)
        else:
            # 初期表示処理
            return self.init(request)
    
    def init(self, request):
        '''
        初期表示処理
        '''
        context = {}

        # サービスの実行
        dto = self.sakuhinTagBindService.initialize('m_sakuhin_tag_map')

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)

        # 組み込みタグ用
        context['object_to_html'] = dto

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)


    # ポスト通信（削除処理）
    def post(self, request):

        # 非同期処理
        json.dumps({}, default=self.json_serial)
        return JsonResponse(dto, safe=False)

    def ajax(self, request):
        '''
        非同期処理
        '''
        dto = {}

        # 更新ユーザの姓名取得
        full_name = request.user.get_full_name()

        # サービスの実行
        # TODO;タグ紐づけ情報表示

        # 関連タイトルモーダル検索時
        if 'title-modal' in request.GET:
            title_name = request.GET.get('title-name')
            # タイトルカテゴリを取得
            category = request.GET.get('category')
            category_list = json.loads(category)

            dto = self.sakuhinTagBindService.getTitleByName(title_name,category_list)

        # # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

