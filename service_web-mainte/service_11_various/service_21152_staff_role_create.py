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

class StaffRoleCreateService(ServiceMain):

    # スタッフ役割マスタテーブル用DAO
    dao_m_staff_role = DaoMStaffRole()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self):

        # m_staff_roleに存在するスタッフ役割コードの最大値を取得
        new_staff_role_code = self.dao_m_staff_role.selectMaxStaffRoleCode()
        # 最大値+1を0埋めする（新規スタッフ役割コード）
        new_staff_role_code = str(int(new_staff_role_code)+1).zfill(5)

        # 領域用DTOを画面DTOに詰める
        return self.unpack({'form':{'staff_role_code':new_staff_role_code}})

    '''スタッフ役割マスタ作成処理'''
    def createStaffRoleData(self,request):

        # POST内容をフォームに設定
        form = DtoStaffRoleCreateForm(request.POST.copy())
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # Dao登録用entityを作成
            entity = self.createDtoForInsert(form,full_name)
            # スタッフ役割マスタの登録
            try :
                self.dao_m_staff_role.insertStaffRole(entity)
            except DaoMStaffRole.DuplicateStaffRoleCodeException as e:
                # スタッフ役割コード重複によりエラーの場合
                # m_staff_roleに存在するスタッフ役割コードの最大値を取得
                new_staff_role_code = self.dao_m_staff_role.selectMaxStaffRoleCode()
                # 最大値+1を0埋めする（新規スタッフ役割コード）
                new_staff_role_code = str(int(new_staff_role_code)+1).zfill(5)
                form.data['staff_role_code'] = new_staff_role_code
                return self.unpack({'is_error':True,'form':form.data,'insert_error_staff_rolecode':True})

            except DaoMStaffRole.DuplicateStaffRoleNameException as e:
                # スタッフ役割名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_staff_rolename':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_staff_role','追加',form.cleaned_data['staff_role_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})

        else :
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にスタッフ役割マスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name):
        return {
            'staff_role_code' : form.cleaned_data['staff_role_code'], # スタッフ役割コード
            'staff_role_name' : form.cleaned_data['staff_role_name'], # スタッフ役割名
            'full_name' : full_name, # 作成者/更新者
            }