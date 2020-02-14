import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView
from admin_app.service.service_01_ip_sakuhin.service_20114_ip_bind import IpBindService


class IpBindView(ListView):

    #サービスクラス
    ipBindService = IpBindService()
    #テンプレート
    template_name = 'admin_app/01_ip_sakuhin/20114_ip_bind.html'

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
        dto = self.ipBindService.initialize('m_ip_map')

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        return render(request, self.template_name, context)

    def ajax(self, request):
        '''
        非同期処理(IPマスタデータ取得)
        '''
        dto = {}

        # 更新ユーザの姓名取得
        full_name = request.user.get_full_name()

        # サービスの実行
        # IPマスタデータ検索時
        if 'select-ip-modal' in request.GET:
            ip_name = request.GET.get('ip-name')
            dto = self.ipBindService.getIpData(ip_name)

        # 関連作品検索時
        if 'select-sakuhin-list' in request.GET:
            ip_code = request.GET.get('ip-code')
            dto = self.ipBindService.getConnectionSakuhinListData(ip_code)

        # 関連作品紐付け解除時
        if 'delete-sakuhin' in request.GET:
            # 紐付けID・IPコードを取得
            map_id = request.GET.get('ip-map-id')
            ip_code = request.GET.get('ip-code')
            # 更新履歴用IP名・作品名を取得
            ip_name = request.GET.get('ip-name')
            sakuhin_name = request.GET.get('sakuhin-name')

            dto = self.ipBindService.delConnectionSakuhin(full_name,map_id,ip_code,ip_name,sakuhin_name)

        # 関連作品検索時（関連作品モーダル）
        if 'sakuhin-modal' in request.GET:
            sakuhin_name = request.GET.get('sakuhin-name')
            dto = self.ipBindService.getConnectionSakuhinModalData(sakuhin_name)

        # 関連作品追加時（関連作品一覧再検索）
        if 'add-sakuhin' in request.GET:
            # 作品コード取得
            sakuhin_code = request.GET.get('sakuhin-code')
            sakuhin_code_lst = json.loads(sakuhin_code)
        
            # IPコード・IP名取得
            ip_code = request.GET.get('ip-code')
            ip_name = request.GET.get('ip-name')

            dto = self.ipBindService.addConnectionSakuhin(sakuhin_code_lst,ip_code,ip_name,full_name)

        # 関連IPマスタデータ検索時
        if 'select-ip-list' in request.GET:
            sakuhin_code = request.GET.get('sakuhin-code')
            dto = self.ipBindService.getIpBySakuhinCode(sakuhin_code)

        # 関連IP紐付け解除時
        if 'delete-ip' in request.GET:
            # 紐付け作品コードを取得
            map_id = request.GET.get('ip-map-id')
            # 作品コード取得
            sakuhin_code = request.GET.get('sakuhin-code')
            # 更新履歴用IP名・作品名を取得
            ip_name = request.GET.get('ip-name')
            sakuhin_name = request.GET.get('sakuhin-name')

            dto = self.ipBindService.delConnectionIp(full_name,map_id,sakuhin_code,ip_name,sakuhin_name)

        # 関連IP検索時（関連IPモーダル）
        if 'ip-modal' in request.GET:
            ip_name = request.GET.get('ip-name')
            dto = self.ipBindService.getIpData(ip_name)


        # 関連IP追加時（関連IP一覧再検索）
        if 'add-ip' in request.GET:
            # IPコード取得
            ip_code = request.GET.get('ip-code')
            ip_code_lst = json.loads(ip_code)
        
            # 作品コード・作品名取得
            sakuhin_code = request.GET.get('sakuhin-code')
            sakuhin_name = request.GET.get('sakuhin-name')

            dto = self.ipBindService.addConnectionIp(ip_code_lst,sakuhin_code,sakuhin_name,full_name)


        # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)

