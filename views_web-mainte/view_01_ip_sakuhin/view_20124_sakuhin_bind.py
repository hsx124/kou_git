import csv
import json
import urllib
import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse

from admin_app.views.view_main import MainView
from admin_app.views.view_list import ListView
from admin_app.service.service_01_ip_sakuhin.service_20124_sakuhin_bind import SakuhinBindService


class SakuhinBindView(ListView):
    #サービスクラス
    sakuhinBindService = SakuhinBindService()
    #テンプレート
    template_name = 'admin_app/01_ip_sakuhin/20124_sakuhin_bind.html'

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
        dto = self.sakuhinBindService.initialize('m_sakuhin_map')

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
        #作品検索時（作品モーダル）
        if 'sakuhin-modal' in request.GET:
            sakuhin_name = request.GET.get('sakuhin-name')
            dto = self.sakuhinBindService.getSakuhinModalData(sakuhin_name)

        # 関連タイトル一覧検索時
        if 'title-list' in request.GET:
            sakuhin_code = request.GET.get('sakuhin-code')
            dto = self.sakuhinBindService.getTitleBySakuhinCode(sakuhin_code)

        # 関連タイトルモーダル検索時
        if 'title-modal' in request.GET:
            title_name = request.GET.get('title-name')
            # タイトルカテゴリを取得
            category = request.GET.get('category')
            category_list = json.loads(category)

            dto = self.sakuhinBindService.getTitleByName(title_name,category_list)

        # 関連タイトル一覧紐付け解除
        if 'delete-title' in request.GET:
            # 作品紐付け解除ID
            sakuhin_map_id = request.GET.get('sakuhin-map-id')
            # 作品コード（関連タイトル一覧データ再検索用）
            sakuhin_code = request.GET.get('sakuhin-code')
            # 作品名（更新履歴DB更新用）
            sakuhin_name = request.GET.get('sakuhin-name')
            # タイトル名（更新履歴DB更新用）
            title_name = request.GET.get('title-name')
            # カテゴリ名（更新履歴DB更新用）
            category_name = request.GET.get('category-name')

            dto = self.sakuhinBindService.delConnectionTitle(full_name,sakuhin_map_id,sakuhin_code,sakuhin_name,title_name,category_name)

        # 関連タイトル追加処理
        if 'add-title' in request.GET:
            # 作品コード（作品紐付けテーブル登録用）
            sakuhin_code = request.GET.get('sakuhin-code')
            # 作品名（作品紐付けテーブル登録用・更新履歴DB更新用）
            sakuhin_name = request.GET.get('sakuhin-name')

            # タイトルコード（作品紐付けテーブル登録用・更新履歴DB更新用）
            title_code_list = json.loads(request.GET.get('title-code'))
            # カテゴリコード（作品紐付けテーブル登録用）
            category_code_list = json.loads(request.GET.get('category-code'))
            # タイトル名（更新履歴DB更新用）
            title_name_list = json.loads(request.GET.get('title-name'))
            # カテゴリ名（更新履歴DB更新用）
            category_name_list = json.loads(request.GET.get('category-name'))

            dto = self.sakuhinBindService.addConnectionTitle(full_name,title_code_list,category_code_list,sakuhin_code,sakuhin_name,title_name_list,category_name_list)

        #Twitter一覧関連作品検索時
        if 'twitter-list' in request.GET:
            sakuhin_code = request.GET.get('sakuhin-code')
            dto = self.sakuhinBindService.getTwitterListData(sakuhin_code)

        #Twitter検索時（Twitterモーダル）
        if 'twitter-modal' in request.GET:
            twitter_name = request.GET.get('twitter-name')
            dto = self.sakuhinBindService.getTwitterModalData(twitter_name)

        # 作品に関連Twitter紐付け解除
        if 'del-twitter-sakuhin' in request.GET:
            # 作品紐付け解除ID
            sakuhin_map_id = request.GET.get('sakuhin-map-id')
            # 作品コード（関連タイトル一覧データ再検索用）
            sakuhin_code = request.GET.get('sakuhin-code')

            # アカウント名（更新履歴DB更新用）
            account_name = request.GET.get('account-name')
            # 作品名（更新履歴DB更新用）
            sakuhin_name = request.GET.get('sakuhin-name')

            dto = self.sakuhinBindService.delTwitterSakuhin(full_name,sakuhin_map_id,sakuhin_code,account_name,sakuhin_name)

        # Twitterの関連作品追加時（Twitter）
        if 'add-twitter-sakuhin' in request.GET:
            # 作品コード取得
            sakuhin_code = request.GET.get('sakuhin-code')
            sakuhin_name = request.GET.get('sakuhin-name')
            # Twitterコード・Twitter名取得
            twitter_code = request.GET.get('twitter-code')
            account_name = request.GET.get('account-name')
            main_flg = request.GET.get('main-flg')

            dto = self.sakuhinBindService.addTwitterSakuhin(full_name,sakuhin_code,sakuhin_name,twitter_code,account_name,main_flg)

        #Game検索時（Gameモーダル）
        if 'game-modal' in request.GET:
            game_name = request.GET.get('game-name')
            dto = self.sakuhinBindService.getGameModalData(game_name)

        #Game一覧関連作品検索時
        if 'game-list' in request.GET:
            game_code = request.GET.get('game-code')
            dto = self.sakuhinBindService.getGameListData(game_code)

        # gameに関連作品紐付け解除
        if 'del-game-sakuhin' in request.GET:
            # 作品紐付け解除ID
            sakuhin_map_id = request.GET.get('sakuhin-map-id')
            # gameコード（関連タイトル一覧データ再検索用）
            game_code = request.GET.get('game-code')
            # gameト名（更新履歴DB更新用）
            game_name = request.GET.get('game-name')
            # 作品名（更新履歴DB更新用）
            sakuhin_name = request.GET.get('sakuhin-name')

            dto = self.sakuhinBindService.delGameSakuhin(full_name,sakuhin_map_id,game_code,game_name,sakuhin_name)

        # Gameの関連作品追加時（Game）
        if 'add-game-sakuhin' in request.GET:
            # 作品コード取得
            sakuhin_code_list = json.loads(request.GET.get('sakuhin-code'))
            # Gameコード・Game名取得
            game_code = request.GET.get('game-code')
            game_name = request.GET.get('game-name')

            dto = self.sakuhinBindService.addGameSakuhin(full_name,sakuhin_code_list,game_code,game_name)

        # # 非同期処理
        json.dumps(dto, default=self.json_serial)
        return JsonResponse(dto, safe=False)


