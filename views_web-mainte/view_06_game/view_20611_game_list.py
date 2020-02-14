import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView



class GameListView(ListView):

    #サービスクラス

    #テンプレート
    template_name = 'admin_app/06_game/20611_game_list.html'

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

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps({}, default=self.json_serial)

        # 組み込みタグ用
        context['object_to_html'] = {}

        if 'show_msg' in request.session:
            context['show_msg'] = request.session['show_msg']
            del request.session['show_msg']

        return render(request, self.template_name, context)


    # ポスト通信（削除処理）
    def post(self, request):

        # 非同期処理
        json.dumps({}, default=self.json_serial)
        return JsonResponse(dto, safe=False)


