import json
from datetime import date, datetime
from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_m_mobile_app import DaoMMobileApp
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_list import DtoList
from admin_app.dto.dto_04_app.dto_20412_app_create import AppCreateForm
from admin_app.dto.dto_04_app.dto_20413_app_update import DtoAppUpdate
from admin_app.service.service_main import ServiceMain

class AppUpdateService(ServiceMain):

    # アプリマスタ
    dao_m_mobile_app = DaoMMobileApp()

    # 変更履歴
    dao_t_update_history = DaoTUpdateHistory()

    def bizProcess(self, ipcode, appname):
        '''
        初期描画
        '''

        # アプリマスタレコードを取得
        app_update_form =self.unpack(self.mapping(DtoAppUpdate.DtoAppUpdateData, self.dao_m_mobile_app.selectAppByIpCodeAppName(ipcode,appname)))

        return self.unpack({'form':app_update_form[0]})

    def updateMMobileApp(self, request, ipcode, appname):

        # POST内容と受信したキービジュアルをフォームに設定
        form = AppCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()

            # データ取得
            entity = self.createDtoForUpdate(form, full_name, ipcode, appname)

            # アプリマスタの登録
            try : 
                self.dao_m_mobile_app.updateMMobileApp(entity)
            except DaoMMobileApp.DuplicateAppIdException as e:
                return self.unpack({'is_error':True,'form':form.data,'insert_error_appid':True})
            except DaoMMobileApp.DuplicateAppNameException as e:
                return self.unpack({'is_error':True,'form':form.data,'insert_error_appname':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_mobile_app','編集',form.cleaned_data['app_name'],'',full_name)
            self.dao_t_update_history.insertTChangeManagement(entity)
            return self.unpack({'is_error':False})
        
        else :
            # 入力チェックNG

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})


    def createDtoForUpdate(self, form, full_name, ip_code, app_name):
        '''
        DAO編集用にアプリマスタエンティティを作成
        '''

        # サービス終了フラグ判定
        # システム日付＞サービス終了日の場合、終了フラグをTRUE
        is_working = False
        if(None != form.cleaned_data['service_end_date']):

            today = date.today()
            today = datetime.strftime(today, '%Y/%m/%d')
            end_date = form.cleaned_data['service_end_date']
            end_date = datetime.strftime(end_date, '%Y/%m/%d')
            if(today > end_date):
                is_working = True

        return {
                'app_name' : form.cleaned_data['app_name'],  # アプリ名
                'app_id_ios' : form.cleaned_data['app_id_ios'], # アプリID_iOS
                'app_id_android' : form.cleaned_data['app_id_android'], # アプリID_Android
                'distributor_name' : form.cleaned_data['distributor_name'], # 販売元
                'is_working' : is_working, # サービス終了フラグ
                'service_start_date' : form.cleaned_data['service_start_date'], # サービス開始年月日
                'service_end_date' : form.cleaned_data['service_end_date'], # サービス終了年月日
                'full_name' : full_name, # 更新者

                'get_ip_code' : ip_code,            # IPコード(レコード特定用)
                'get_app_name' : app_name            # アプリ名(レコード特定用)
                }