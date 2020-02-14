import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dao.dao_m_media import DaoMMedia

from admin_app.dto.dto_11_various.dto_21112_media_create import DtoMediaCreateForm
from admin_app.dto.dto_11_various.dto_21113_media_update import DtoMediaUpdate

class MediaUpdateService(ServiceMain):

    # 掲載媒体マスタテーブル用DAO
    dao_m_media = DaoMMedia()
    # 更新履歴
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self, media_code):

        context = {}

        # 画面に掲載媒体マスタ情報を設定
        # 掲載媒体コードに紐づく画面要素を取得
        param = {'media_code':media_code}
        media_update_form = self.unpack(self.mapping(DtoMediaUpdate.DtoMediaUpdateData, self.dao_m_media.selectUpdateData(param)))

        if media_update_form:
            return self.unpack({'value_not_found':False,'form':media_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})
        

    '''掲載媒体マスタ更新処理'''
    def updateMediaData(self, request):
        
        # POST内容と受信したキービジュアルをフォームに設定
        form = DtoMediaCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # 掲載媒体マスタの登録
            try:
                self.dao_m_media.update(entity)
            except DaoMMedia.DuplicateMediaNameException as e:
                # 掲載媒体名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_media','編集',form.cleaned_data['media_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO更新用に掲載媒体マスタエンティティを作成'''
    def createDtoForUpdate(self,form, full_name):
        return {
                'media_code' : form.cleaned_data['media_code'], # 掲載媒体コード
                'media_name' : form.cleaned_data['media_name'], # 掲載媒体名
                'show_flg' : form.cleaned_data['show_flg'], # 表示/非表示
                'priority' : form.cleaned_data['priority'], # 優先順位
                'full_name' : full_name, # 作成者/更新者
                }