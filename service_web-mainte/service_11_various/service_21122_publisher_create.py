import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_publisher import DaoMPublisher
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_11_various.dto_21122_publisher_create import DtoPublisherCreateForm



class PublisherCreateService(ServiceMain):

    # 出版社マスタテーブル用DAO
    dao_m_publisher = DaoMPublisher()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self):

        # m_publisherに存在する出版社コードの最大値を取得
        new_publisher_code = self.dao_m_publisher.selectMaxPublisherCode()
        # 最大値+1を0埋めする（新規出版社コード）
        new_publisher_code = str(int(new_publisher_code)+1).zfill(5)
            
        return self.unpack({'form':{'publisher_code':new_publisher_code}})

    '''出版社マスタ作成処理'''
    def createPublisherData(self,request):

        # POST内容をフォームに設定
        form = DtoPublisherCreateForm(request.POST.copy())
        
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # Dao登録用entityを作成
            entity = self.createDtoForInsert(form,full_name)

            # 出版社マスタの登録
            try : 
                self.dao_m_publisher.insert(entity)
            except DaoMPublisher.DuplicatePublisherCodeException as e:
                # 出版社コード重複によりエラーの場合

                # m_publisherに存在する出版社コードの最大値を取得
                new_publisher_code = self.dao_m_publisher.selectMaxPublisherCode()
                # 最大値+1を0埋めする（新規出版社コード）
                max_code = str(int(new_publisher_code)+1).zfill(5)

                form.data['publisher_code'] = max_code
                return self.unpack({'is_error':True,'form':form.data,'insert_error_publishercode':True})

            except DaoMPublisher.DuplicatePublisherNameException as e:
                # 出版社名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_publishername':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_publisher','追加',form.cleaned_data['publisher_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})

        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用に出版社マスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name):
        return {
            'publisher_code' : form.cleaned_data['publisher_code'], # 出版社コード
            'publisher_name' : form.cleaned_data['publisher_name'], # 出版社名
            'full_name' : full_name, # 作成者/更新者
            }