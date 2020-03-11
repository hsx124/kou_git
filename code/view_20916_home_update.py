import json

from django.shortcuts import redirect,render
from admin_app.views.view_main import MainView

from admin_app.service.service_09_home.service_20916_home_update import HomeUpdateService
from django.db import transaction

class HomeUpdateView(MainView):

    #サービスクラス
    homeUpdateService = HomeUpdateService()
    
    #テンプレート
    template_name = 'admin_app/09_home/20916_home_update.html'

    def get(self,request):
        context = {}
        dto = {}

        # パラメータ名が正しい場合
        if 'preview' in request.GET and request.GET['preview'].isnumeric():
            preview = request.GET['preview']
            position = preview
            #サービスの実行:サービスの業務プロセス呼ぶ
            dto = self.homeUpdateService.initialize(position)
            # dto = {'dto':dto,'position':position}
            dto['position'] = position

            # 編集対象存在しない場合、一覧画面に戻る
           
            if dto['value_not_found']:
                # positionコード存在しないる場合
                # 「HOME画面」へリダイレクト
                response = redirect('admin_app:20915_home_list')

                # セッションを保存
                request.session['show_msg'] = {
                    'targetname' : 'バナーリンク編集情報',
                    'status' : 'value_error'}
                
                return response
            else:
                # 編集対象存在する場合、編集画面へ遷移する
                # javascriptデータ連携用
                context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)

                # 組み込みタグ用
                context['object_to_html'] =dto

                return render(request, self.template_name, context)

        else:
           # パラメータ名が不正な場合
            # 「Home画面」へリダイレクト
            response = redirect('admin_app:20915_home_list')
            # セッションを保存
            request.session['show_msg'] = {'status' : 'param_error'}

            return response 

    @transaction.atomic
    def post(self,request):
        context = {}
        position = request.POST['position']
        banner_title = request.POST['banner_title']
        banner_detail = request.POST['banner_detail']
        external_site = ''
        media_report_code = ''
        media_report_name = ''
        is_checked = False
        if 'url_checkbox' in request.POST:
            # 外部サイトの時
            external_site = request.POST['banner_url']
            media_report_code = ''
            media_report_name = ''
            is_checked = True
            
        else:
            # 白書の時
            external_site = ''
            media_report_code = request.POST['media_report_code']
            media_report_name = request.POST['banner_hakusho']
            
        dto = self.homeUpdateService.updateBannerData(position,banner_title,banner_detail,external_site,media_report_code,media_report_name,is_checked,request)
        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
        # 組み込みタグ用
        context['object_to_html'] = dto

        if dto['is_error']:
            return render(request, self.template_name, context)
        else:
            # エラーがない場合、且つ、保存ボタンを押下の場合、
            # 「IP情報一覧画面」へリダイレクト
            response = redirect('admin_app:20915_home_list')
            # セッションを保存
            request.session['show_msg'] = {
                'targetname' : request.POST.get('banner_title'),
                'status' : 'update'
            }
        
        return response

