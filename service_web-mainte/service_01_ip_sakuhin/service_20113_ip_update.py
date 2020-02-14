import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_ip import DaoMIp
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_01_ip_sakuhin.dto_20112_ip_create import DtoIpCreateForm
from admin_app.dto.dto_01_ip_sakuhin.dto_20113_ip_update import DtoIpUpdate

class IpUpdateService(ServiceMain):

    # IPマスタテーブル用DAO
    dao_m_ip = DaoMIp()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self,ip_code):

        context = {}

        # 画面にIPマスタ情報を設定
        # IPコードに紐づく画面要素を取得
        param = {'ip_code':ip_code}
        ip_update_form = self.unpack(self.mapping(DtoIpUpdate.DtoIpUpdateData, self.dao_m_ip.selectUpdateData(param)))
        
        if ip_update_form:
            return self.unpack({'value_not_found':False,'form':ip_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})


    '''IPマスタ更新処理'''
    def updateIpData(self, request):

        form = DtoIpCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # IPマスタの登録
            try:
                self.dao_m_ip.update(entity)
            except DaoMIp.DuplicateIpNameException as e:
                # IP名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_name':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_ip','編集',form.cleaned_data['ip_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})
    '''DAO登録用にIPマスタエンティティを作成'''
    def createDtoForUpdate(self,form,full_name):
        return {
            'ip_code' : form.cleaned_data['ip_code'], # IPコード
            'ip_name' : form.cleaned_data['ip_name'], # IP名
            'ip_kana_name' : form.cleaned_data['ip_kana_name'], # IPかな名
            'ip_control_flg' : form.cleaned_data['ip_control_flg'], # IP管理フラグ
            'full_name' : full_name, # 作成者/更新者
            }