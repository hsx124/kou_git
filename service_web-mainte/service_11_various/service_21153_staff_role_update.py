import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_staff_role import DaoMStaffRole
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_11_various.dto_21151_staff_role_list import DtoStaffRoleList
from admin_app.dto.dto_11_various.dto_21152_staff_role_create import DtoStaffRoleCreateForm
from admin_app.dto.dto_11_various.dto_21153_staff_role_update import DtoStaffRoleUpdate

class StaffRoleUpdateService(ServiceMain):

    # スタッフ役割マスタテーブル用DAO
    dao_m_staff_role = DaoMStaffRole()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self,staff_role_code):

        context = {}
        # 画面にスタッフ役割マスタ情報を設定
        # スタッフ役割コードに紐づく画面要素を取得
        param = {'staff_role_code':staff_role_code}
        staff_role_update_form = self.unpack(self.mapping(DtoStaffRoleUpdate.DtoStaffRoleUpdateData, self.dao_m_staff_role.selectUpdateData(param)))

        if staff_role_update_form:
            return self.unpack({'value_not_found':False,'form':staff_role_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    '''スタッフ役割マスタ更新処理'''
    def updateStaffRoleData(self, request):

        form = DtoStaffRoleCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # スタッフ役割マスタの登録
            try:
                self.dao_m_staff_role.updateStaffRole(entity)
            except DaoMStaffRole.DuplicateStaffRoleNameException as e:
                # スタッフ役割名重複によりエラーの場合

                return self.unpack({'is_error':True,'form':form.data,'update_error':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_staff_role','編集',form.cleaned_data['staff_role_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にスタッフ役割マスタエンティティを作成'''
    def createDtoForUpdate(self,form,full_name):
        return {
            'staff_role_code' : form.cleaned_data['staff_role_code'], # スタッフ役割コード
            'staff_role_name' : form.cleaned_data['staff_role_name'], # スタッフ役割名
            'full_name' : full_name, # 作成者/更新者
            }