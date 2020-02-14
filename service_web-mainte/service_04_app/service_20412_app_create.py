import json
from datetime import date, datetime
from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_m_mobile_app import DaoMMobileApp
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_list import DtoList
from admin_app.dto.dto_04_app.dto_20412_app_create import AppCreateForm

from admin_app.service.service_main import ServiceMain

class AppCreateService(ServiceMain):

    # IPマスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()

    # アプリマスタ
    dao_m_mobile_app = DaoMMobileApp()

    # 変更履歴
    dao_t_update_history = DaoTUpdateHistory()

    def bizProcess(self, ipcode):
        '''
        初期描画
        '''

        # IPコードからIPを検索
        ip_search_result = self.unpack(self.mapping(DtoList.DtoIpSearchResult, self.dao_m_sakuhin.selectIpMasterByIpCode(ipcode)))

        return self.unpack({'form':{'ip_code':ipcode, 'ip_name':ip_search_result[0]['ip_name']}})

    def createMMobileApp(self, request, appname):

        # POST内容と受信したキービジュアルをフォームに設定
        form = AppCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
        
            entity = self.createDtoForInsert(form,full_name)

            # アプリマスタの登録
            try : 
                self.dao_m_mobile_app.insertMMobileApp(entity)
            except DaoMMobileApp.DuplicateAppIdException as e:
                return self.unpack({'is_error':True,'form':form.data,'insert_error_appid':True})
            except DaoMMobileApp.DuplicateAppNameException as e:
                return self.unpack({'is_error':True,'form':form.data,'insert_error_appname':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_mobile_app','追加',form.cleaned_data['app_name'],'',full_name)
            self.dao_t_update_history.insertTChangeManagement(entity)
            return self.unpack({'is_error':False})
        else :
            # 入力チェックNG

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    def createDtoForInsert(self,form,full_name):
        '''
        DAO登録用にアプリマスタエンティティを作成
        '''

        # サービス終了フラグ判定
        # システム日付＞サービス終了日の場合、終了フラグを設定
        is_working = False
        if(None != form.cleaned_data['service_end_date']):

            today = date.today()
            today = datetime.strftime(today, '%Y/%m/%d')
            end_date = form.cleaned_data['service_end_date']
            end_date = datetime.strftime(end_date, '%Y/%m/%d')
            if(today >= end_date):
                is_working = True

        return {
                'ip_code' : form.cleaned_data['ip_code'], # IPコード
                'app_name' : form.cleaned_data['app_name'],  # アプリ名
                'app_id_ios' : form.cleaned_data['app_id_ios'], # アプリID_iOS
                'app_id_android' : form.cleaned_data['app_id_android'], # アプリID_Android
                'distributor_name' : form.cleaned_data['distributor_name'], # 販売元
                'is_working' : is_working, # サービス終了フラグ
                'service_start_date' : form.cleaned_data['service_start_date'], # サービス開始年月日
                'service_end_date' : form.cleaned_data['service_end_date'], # サービス終了年月日
                'full_name' : full_name, # 更新者
                }
