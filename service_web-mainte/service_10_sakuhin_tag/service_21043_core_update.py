import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_core import DaoMCore
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_10_sakuhin_tag.dto_21041_core_list import DtoCoreList
from admin_app.dto.dto_10_sakuhin_tag.dto_21042_core_create import DtoCoreCreateForm
from admin_app.dto.dto_10_sakuhin_tag.dto_21043_core_update import DtoCoreUpdate

class CoreUpdateService(ServiceMain):

    # コアマスタテーブル用DAO
    dao_m_core = DaoMCore()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self,core_code):

        context = {}
        # 画面にコアマスタ情報を設定
        # コアコードに紐づく画面要素を取得
        param = {'core_code':core_code}
        core_update_form = self.unpack(self.mapping(DtoCoreUpdate.DtoCoreUpdateData, self.dao_m_core.selectUpdateData(param)))

        if core_update_form:
            return self.unpack({'value_not_found':False,'form':core_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    '''コアマスタ更新処理'''
    def updateCoreData(self, request):

        form = DtoCoreCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # コアマスタの登録
            try:
                self.dao_m_core.updateCore(entity)
            except DaoMCore.DuplicateCoreNameException as e:
                # コア名重複によりエラーの場合

                return self.unpack({'is_error':True,'form':form.data,'update_error':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_core','編集',form.cleaned_data['core_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にコアマスタエンティティを作成'''
    def createDtoForUpdate(self,form,full_name):
        return {
            'core_code' : form.cleaned_data['core_code'], # コアコード
            'core_name' : form.cleaned_data['core_name'], # コア名
            'full_name' : full_name, # 作成者/更新者
            }