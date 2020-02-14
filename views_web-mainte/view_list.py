import csv
import json
import urllib
from datetime import date, datetime 
from django.http.response import JsonResponse,HttpResponse
from admin_app.views.view_main import MainView
from admin_app.service.service_list import ServiceList
from admin_app.dto.dto_list import DtoList

import time

class ListView(MainView):

    def changecsvdownload(request):
        '''
        変更履歴CSVダウンロード
        '''
        response = HttpResponse(content_type='text/csv')
        filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        if 'date-start' in request.GET:
            csv_date = ServiceList.changecsvdownloadprocess(ServiceList, request.GET.get('table-name'), request.GET.get('date-start'),request.GET.get('date-end'))
        else:
            csv_date = ServiceList.changecsvdownloadprocess(ServiceList, request.GET.get('table-name'))

        #csv書き込み
        writer = csv.writer(response)

        # ヘッダー出力
        header = ['更新日時', '更新者', '更新マスタ', '更新対象', '操作内容', '備考']
        writer.writerow(header)

        for row in csv_date:
            #日付形式フォーマット変換
            update_date = row.update_date.strftime('%Y/%m/%d %H:%M:%S.%f')
            update_user = row.update_user
            update_table = row.update_table
            target_name = row.target_name
            operation = row.operation
            remarks = row.remarks

            row_list = DtoList.DtoUpdateHistoryCsv(update_date, update_user, update_table, target_name, operation, remarks)
            writer.writerow(row_list)
    
        return response
    
    def csvDateFormat(d):
        '''
        日付形式フォーマット変換
        '''
        if isinstance(d, datetime):
            return d.strftime('%Y/%m/%d %H:%M:%S.%f')
        elif isinstance(d, date):
            return d.strftime('%Y/%m/%d')
        else:
            # 日付以外は変換せず返却する
            return d
