import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dao.dao_m_publisher import DaoMPublisher

from admin_app.dto.dto_11_various.dto_21122_publisher_create import DtoPublisherCreateForm
from admin_app.dto.dto_11_various.dto_21123_publisher_update import DtoPublisherUpdate

class PublisherUpdateService(ServiceMain):

    # 出版社マスタテーブル用DAO
    dao_m_publisher = DaoMPublisher()
    # 更新履歴
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self, publisher_code):

        context = {}

        # 画面に出版社マスタ情報を設定
        # 出版社コードに紐づく画面要素を取得
        param = {'publisher_code':publisher_code}
        publisher_update_form = self.unpack(self.mapping(DtoPublisherUpdate.DtoPublisherUpdateData, self.dao_m_publisher.selectUpdateData(param)))
        
        if publisher_update_form:
            return self.unpack({'value_not_found':False,'form':publisher_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    '''出版社マスタ更新処理'''
    def updatePublisherData(self, request):

        # POST内容と受信したキービジュアルをフォームに設定
        form = DtoPublisherCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # 出版社マスタの登録
            try:
                self.dao_m_publisher.update(entity)
            except DaoMPublisher.DuplicatePublisherNameException as e:
                # 出版社名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_publisher','編集',form.cleaned_data['publisher_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO更新用に出版社マスタエンティティを作成'''
    def createDtoForUpdate(self,form, full_name):
        return {
                'publisher_code' : form.cleaned_data['publisher_code'], # 出版社コード
                'publisher_name' : form.cleaned_data['publisher_name'], # 出版社名
                'full_name' : full_name, # 作成者/更新者
                }