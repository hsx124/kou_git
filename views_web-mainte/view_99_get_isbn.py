import traceback
from django.http.response import JsonResponse, HttpResponse
from admin_app.views.view_main import MainView
from admin_app.service.service_99_get_isbn import GetIsbnService


class GetIsbnView(MainView):

    # サービスクラス
    getIsbnService = GetIsbnService()

    def get(self, request):
        if request.is_ajax():
            # 非同期処理
            return self.ajax(request)

    def ajax(self, request):
        try:
            result = self.getIsbnService.getIsbn(request.GET['input-book-name'])
        except:
            print('異常終了')
            print(traceback.format_exc())
            result=[]
        else:
            print('正常終了')
        finally:
            return JsonResponse(result, safe=False)
