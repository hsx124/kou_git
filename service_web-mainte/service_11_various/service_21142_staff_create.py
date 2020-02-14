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

class StaffCreateService(ServiceMain):

    # スタッフマスタテーブル用DAO
    dao_m_staff = DaoMStaff()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self):

        # m_staffに存在するスタッフコードの最大値を取得
        new_staff_code = self.dao_m_staff.selectMaxStaffCode()
        # 最大値+1を0埋めする（新規スタッフコード）
        new_staff_code = str(int(new_staff_code)+1).zfill(5)

        # 領域用DTOを画面DTOに詰める
        return self.unpack({'form':{'staff_code':new_staff_code}})

    '''スタッフマスタ作成処理'''
    def createStaffData(self,request):

        # POST内容をフォームに設定
        form = DtoStaffCreateForm(request.POST.copy())
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # Dao登録用entityを作成
            entity = self.createDtoForInsert(form,full_name)
            # スタッフマスタの登録
            try :
                self.dao_m_staff.insertStaff(entity)
            except DaoMStaff.DuplicateStaffCodeException as e:
                # スタッフコード重複によりエラーの場合
                # m_staffに存在するスタッフコードの最大値を取得
                new_staff_code = self.dao_m_staff.selectMaxStaffCode()
                # 最大値+1を0埋めする（新規スタッフコード）
                new_staff_code = str(int(new_staff_code)+1).zfill(5)
                form.data['staff_code'] = new_staff_code
                return self.unpack({'is_error':True,'form':form.data,'insert_error_staffcode':True})

            except DaoMStaff.DuplicateStaffNameException as e:
                # スタッフ名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_staffname':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_staff','追加',form.cleaned_data['staff_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})

        else :
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にスタッフマスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name):
        return {
            'staff_code' : form.cleaned_data['staff_code'], # スタッフコード
            'staff_name' : form.cleaned_data['staff_name'], # スタッフ名
            'past_sakuhin' : form.cleaned_data['past_sakuhin'], # 過去作品
            'remarks' : form.cleaned_data['remarks'], # 備考
            'full_name' : full_name, # 作成者/更新者
            }