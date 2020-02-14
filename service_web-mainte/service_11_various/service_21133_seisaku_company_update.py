import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dao.dao_m_seisaku_company import DaoMSeisakuCompany

from admin_app.dto.dto_11_various.dto_21132_seisaku_company_create import DtoSeisakuCompanyCreateForm
from admin_app.dto.dto_11_various.dto_21133_seisaku_company_update import DtoSeisakuCompanyUpdate

class SeisakuCompanyUpdateService(ServiceMain):

    # 制作会社マスタテーブル用DAO
    dao_m_seisaku_company = DaoMSeisakuCompany()
    # 更新履歴
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self, seisaku_company_code):

        context = {}

        # 画面に制作会社マスタ情報を設定
        # 制作会社コードに紐づく画面要素を取得
        param = {'seisaku_company_code':seisaku_company_code}
        seisaku_company_update_form = self.unpack(self.mapping(DtoSeisakuCompanyUpdate.DtoSeisakuCompanyUpdateData, self.dao_m_seisaku_company.selectUpdateData(param)))
        
        if seisaku_company_update_form:
            return self.unpack({'value_not_found':False,'form':seisaku_company_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    '''制作会社マスタ更新処理'''
    def updateSeisakuCompanyData(self, request):

        # POST内容と受信したキービジュアルをフォームに設定
        form = DtoSeisakuCompanyCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # 制作会社マスタの登録
            try:
                self.dao_m_seisaku_company.update(entity)
            except DaoMSeisakuCompany.DuplicateSeisakuCompanyNameException as e:
                # 制作会社名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_name':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_seisaku_company','編集',form.cleaned_data['seisaku_company_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO更新用に制作会社マスタエンティティを作成'''
    def createDtoForUpdate(self,form, full_name):
        return {
                'seisaku_company_code' : form.cleaned_data['seisaku_company_code'], # 制作会社コード
                'seisaku_company_name' : form.cleaned_data['seisaku_company_name'], # 制作会社名
                'full_name' : full_name, # 作成者/更新者
                }