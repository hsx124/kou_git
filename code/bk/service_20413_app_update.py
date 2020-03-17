import json
from datetime import date, datetime
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_04_app.dto_20412_app_create import AppCreateForm
from admin_app.dto.dto_04_app.dto_20413_app_update import DtoAppUpdate
from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_app_title import DaoMAppTitle

class AppUpdateService(ServiceMain):

    # アプリマスタ
    dao_m_app_title = DaoMAppTitle()

    # 変更履歴
    dao_t_update_history = DaoTUpdateHistory()

    def initialize(self, app_code):
        '''
        初期描画
        '''
        context = {}
        # 画面にアプリタイトル基本マスタ情報を設定
        # アプリタイトルコードに紐づく画面要素を取得
        param = {'app_code':app_code}
        app_update_form = self.unpack(self.mapping(DtoAppUpdate.DtoAppUpdateData, self.dao_m_app_title.selectUpdateData(param)))
        
        if app_update_form:
            service_start_yyyymmdd = app_update_form[0]['service_start_yyyymmdd']
            service_end_yyyymmdd = app_update_form[0]['service_end_yyyymmdd']
            if None !=service_start_yyyymmdd and service_start_yyyymmdd !='' :
                service_start = datetime.strptime(app_update_form[0]['service_start_yyyymmdd'],'%Y%m%d')
                app_update_form[0]['service_start_yyyymmdd'] = service_start.strftime('%Y/%m/%d')

            if None != service_end_yyyymmdd and service_end_yyyymmdd != '':
                service_end = datetime.strptime(app_update_form[0]['service_end_yyyymmdd'],'%Y%m%d')
                app_update_form[0]['service_end_yyyymmdd'] =  service_end.strftime('%Y/%m/%d')
            return self.unpack({'value_not_found':False,'form':app_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    def updateAppData(self, form, full_name):

        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # データ取得
            entity = self.createDtoForUpdate(form, full_name)
            # アプリマスタの登録
            try : 
                self.dao_m_app_title.update(entity)
            except DaoMAppTitle.DuplicateAppNameException as e:
                return self.unpack({'is_error':True,'form':form.data,'insert_error_appname':True})
            except DaoMAppTitle.DuplicateAppIosIdException as e:
                return self.unpack({'is_error':True,'form':form.data,'insert_error_app_id_ios':True})
            except DaoMAppTitle.DuplicateAppAndroidIdException as e:
                
                return self.unpack({'is_error':True,'form':form.data,'insert_error_app_id_android':True})
            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_app_title','編集',form.cleaned_data['app_name'],'',full_name)
            self.dao_t_update_history.insert(entity)
            return self.unpack({'is_error':False})
        
        else :
            # 入力チェックNG

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})


    def createDtoForUpdate(self, form, full_name):
        '''
        DAO編集用にアプリマスタエンティティを作成
        '''
        service_start_yyyymmdd = form.cleaned_data['service_start_yyyymmdd']
        service_end_yyyymmdd = form.cleaned_data['service_end_yyyymmdd']
         
        if service_start_yyyymmdd is None :
            service_start_yyyymmdd = ''
        else :
            service_start_yyyymmdd = datetime.strftime(form.cleaned_data['service_start_yyyymmdd'],'%Y%m%d')

        if service_end_yyyymmdd is None:
            service_end_yyyymmdd = ''
        else :
            service_end_yyyymmdd = datetime.strftime(form.cleaned_data['service_end_yyyymmdd'],'%Y%m%d')

        return {
                'app_code' : form.cleaned_data['app_code'],  # アプリ名
                'app_name' : form.cleaned_data['app_name'],  # アプリ名
                'app_id_ios' : form.cleaned_data['app_id_ios'], # アプリID_iOS
                'app_id_android' : form.cleaned_data['app_id_android'], # アプリID_Android
                'hanbai_company_name' : form.cleaned_data['hanbai_company_name'], # 販売元
                'service_start_yyyymmdd' : service_start_yyyymmdd, # サービス開始年月日
                'service_end_yyyymmdd' : service_end_yyyymmdd, # サービス終了年月日
                'full_name' : full_name, # 更新者
                }