import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_staff import DaoMStaff
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_11_various.dto_21141_staff_list import DtoStaffList
from admin_app.dto.dto_11_various.dto_21142_staff_create import DtoStaffCreateForm
from admin_app.dto.dto_11_various.dto_21143_staff_update import DtoStaffUpdate

class StaffUpdateService(ServiceMain):

    # スタッフマスタテーブル用DAO
    dao_m_staff = DaoMStaff()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self,staff_code):

        context = {}
        # 画面にスタッフマスタ情報を設定
        # スタッフコードに紐づく画面要素を取得
        param = {'staff_code':staff_code}
        staff_update_form = self.unpack(self.mapping(DtoStaffUpdate.DtoStaffUpdateData, self.dao_m_staff.selectUpdateData(param)))

        if staff_update_form:
            return self.unpack({'value_not_found':False,'form':staff_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    '''スタッフマスタ更新処理'''
    def updateStaffData(self, request):

        form = DtoStaffCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # スタッフマスタの登録
            try:
                self.dao_m_staff.updateStaff(entity)
            except DaoMStaff.DuplicateStaffNameException as e:
                # スタッフ名重複によりエラーの場合

                return self.unpack({'is_error':True,'form':form.data,'update_error':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_staff','編集',form.cleaned_data['staff_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にスタッフマスタエンティティを作成'''
    def createDtoForUpdate(self,form,full_name):
        return {
            'staff_code' : form.cleaned_data['staff_code'], # スタッフコード
            'staff_name' : form.cleaned_data['staff_name'], # スタッフ名
            'past_sakuhin' : form.cleaned_data['past_sakuhin'], # 過去作品
            'remarks' : form.cleaned_data['remarks'], # 備考
            'full_name' : full_name, # 作成者/更新者
            }