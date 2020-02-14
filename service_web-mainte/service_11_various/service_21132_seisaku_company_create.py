import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_seisaku_company import DaoMSeisakuCompany
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_11_various.dto_21132_seisaku_company_create import DtoSeisakuCompanyCreateForm

class SeisakuCompanyCreateService(ServiceMain):

    # 制作会社マスタテーブル用DAO
    dao_m_seisaku_company = DaoMSeisakuCompany()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self):

        # m_seisaku_companyに存在する制作会社コードの最大値を取得
        new_code = self.dao_m_seisaku_company.selectMaxCode()
        # 最大値+1を0埋めする（新規制作会社コード）
        max_code = str(int(new_code)+1).zfill(5)
            
        return self.unpack({'form':{'seisaku_company_code':max_code}})

    '''制作会社マスタ作成処理'''
    def createSeisakuCompanyData(self,request):

        # POST内容をフォームに設定
        form = DtoSeisakuCompanyCreateForm(request.POST.copy())
        
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # Dao登録用entityを作成
            entity = self.createDtoForInsert(form,full_name)

            # 制作会社マスタの登録
            try : 
                self.dao_m_seisaku_company.insert(entity)
            except DaoMSeisakuCompany.DuplicateSeisakuCompanyCodeException as e:
                # 制作会社コード重複によりエラーの場合

                # m_seisaku_companyに存在する制作会社コードの最大値を取得
                new_code = self.dao_m_seisaku_company.selectMaxCode()
                # 最大値+1を0埋めする（新規制作会社コード）
                max_code = str(int(new_code)+1).zfill(5)

                form.data['seisaku_company_code'] = max_code
                return self.unpack({'is_error':True,'form':form.data,'insert_error_code':True})

            except DaoMSeisakuCompany.DuplicateSeisakuCompanyNameException as e:
                # 制作会社名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_name':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_seisaku_company','追加',form.cleaned_data['seisaku_company_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})

        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用に制作会社マスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name):
        return {
            'seisaku_company_code' : form.cleaned_data['seisaku_company_code'], # 制作会社コード
            'seisaku_company_name' : form.cleaned_data['seisaku_company_name'], # 制作会社名
            'full_name' : full_name, # 作成者/更新者
            }