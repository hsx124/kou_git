import json
from django.http.response import JsonResponse
from django.shortcuts import render
from ipdds_app.views.view_main import MainView
from ipdds_app.service.service_01_home.service_10101_home import HomeService


class HomeView(MainView):

    permission_required = ("app.add_message",)
    # サービスクラス
    homeService = HomeService()
    # テンプレート
    template_name = 'ipdds_app/01_home/10101_home.html'

    def get(self, request):

        if request.is_ajax():
            dto = self.ajax(request)
            return JsonResponse(dto, safe=False)

        else:
            # コンテキストの取得
            context = {}

            # サービスの実行
            dto = self.homeService.bizProcess()

            # javascriptデータ連携用
            context['object_to_javascript'] = json.dumps(dto)
            # 組み込みタグ用
            context['object_to_html'] = dto

            return render(request, self.template_name, context)

    def ajax(self, request):
        return self.homeService.getTagInfo(request.GET.get('sakuhin_code'))
