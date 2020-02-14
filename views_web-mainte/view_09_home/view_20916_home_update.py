import json

from django.shortcuts import redirect,render
from admin_app.views.view_main import MainView

from admin_app.service.service_09_home.service_20916_home_update import HomeUpdateService


class HomeUpdateView(MainView):

    #サービスクラス
    homeUpdateService = HomeUpdateService()
    
    #テンプレート
    template_name = 'admin_app/09_home/20916_home_update.html'

    def get_context_data(self, **kwargs):

        # コンテキストの取得
        context = super().get_context_data(**kwargs)
    
        return  context

    def get(self,request):
        
        context = {}
        dto = {}
        if 'preview' in request.GET:
            preview = request.GET['preview']
            position = preview
            #サービスの実行:サービスの業務プロセス呼ぶ
            dto = self.homeUpdateService.bizProcess(position)
            dto = {'dto':dto,'position':position}

        # javascriptデータ連携用
        context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)

        # 組み込みタグ用
        context['object_to_html'] =dto

        return render(request, self.template_name, context)

    def post(self,request):
        if 'url_checkbox' in request.POST:
            # 外部サイトの時
            dto = self.homeUpdateService.homeUpdateProcess(request.POST['position'],request.POST['banner_title'],request.POST['banner_detail'],request.POST['banner_url'],'','',True,request)
        else:
            # 白書の時
            dto = self.homeUpdateService.homeUpdateProcess(request.POST['position'],request.POST['banner_title'],request.POST['banner_detail'],'',request.POST['banner_hakusho_num'],request.POST['banner_hakusho'],False,request)
        
        if dto['is_error']:
            context = {}
            # javascriptデータ連携用
            context['object_to_javascript'] =  json.dumps(dto, default=self.json_serial)
            # 組み込みタグ用
            context['object_to_html'] = dto
            return render(request, self.template_name, context)
        return redirect('admin_app:20915_home_list')

