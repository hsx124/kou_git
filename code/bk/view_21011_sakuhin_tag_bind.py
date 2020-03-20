import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse
from django.db import transaction
from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView
from admin_app.service.service_10_sakuhin_tag.service_21011_sakuhin_tag_bind import SakuhinTagBindService
from admin_app.service.service_10_sakuhin_tag.service_21021_sakuhin_tag_list import SakuhinTagListService

class SakuhinTagBindView(ListView):

    #サービスクラス
    sakuhinTagBindService = SakuhinTagBindService()
    sakuhinTagListService = SakuhinTagListService()
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


    # # ポスト通信（削除処理）
    # def post(self, request):

    #     # 非同期処理
    #     json.dumps({}, default=self.json_serial)
    #     return JsonResponse(dto, safe=False)

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
        
        if 'category_select' in request.GET:
            title_name = request.GET.get('category_code')
            dto = self.sakuhinTagListService.getSakuhinTagList(title_name)

        if 'tag_name_select' in request.GET:
            tag_code = request.GET.get('tag_code_list')
            tag_code_list=json.loads(tag_code)
            if len(tag_code_list) != 0:
                dto = self.sakuhinTagBindService.getTagNameByCode(tag_code_list)
                
                categoryInfo = tag_code_list
                for code_num in tag_code_list.items():
                   
                    for code_name in dto:                  
                        if code_num[1] == code_name[0]:
                            categoryInfo[code_num[0]] = [code_name[0],code_name[1]]
                        
                dto = categoryInfo
        
        if 'tag_like_search' in request.GET:
            
            tag_name = request.GET.get('tag_name')
            param = {'tag_name' : '%' + tag_name + '%'}
            dto = self.sakuhinTagBindService.getSakuhinTag(param)

        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)
    
    def post(self,request):
        dto = {}
        param = request.POST
        dto=json.loads(param['param'])
        user_name = request.user.get_full_name()
        status = self.sakuhinTagBindService.createInsertOrUpdateData(dto,user_name)

         # セッションを保存
        request.session['show_msg'] = {
            'targetname' : dto['title_name'],
            'status' : status
        }
        # json.dumps(dto, default=self.json_serial)
        # return JsonResponse(dto, safe=False)
        
        response = redirect('admin_app:21011_sakuhin_tag_bind')
        return response
