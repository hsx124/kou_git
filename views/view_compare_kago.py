from ipdds_app.views.view_main import MainView
from django.shortcuts import render,HttpResponse,redirect
from django.http.response import JsonResponse

class CompareKagoView(MainView):

    def set_session(request):
        #session編集できる設定
        request.session.modified = True
        
        #sessionの初期化
        if 'compare_kago' not in request.session:
            dto = []
            request.session['compare_kago'] = []

        #sessionからデータを取得する 
        if 'kago_get' in request.GET:
            dto = request.session['compare_kago']
            return JsonResponse(dto, safe=False)

        #sessionにデータを追加する
        if 'kago_add' in request.POST:
            request.session['compare_kago'].append({'ip_code':request.POST['ip_code'],'ip_name':request.POST['ip_name'],'keyvisual':request.POST['keyvisual']})
            return JsonResponse("success", safe=False)

        #sessionからデータを削除する
        if 'kago_delete' in request.POST:
            request.session['compare_kago'].remove({'ip_code':request.POST['ip_code'],'ip_name':request.POST['ip_name'],'keyvisual':request.POST['keyvisual']})
            return JsonResponse("success", safe=False)

