import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_sakuhin_tag import DaoMSakuhinTag
from admin_app.dao.dao_m_sakuhin_tag_category import DaoMSakuhinTagCategory
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_10_sakuhin_tag.dto_21021_sakuhin_tag_list import DtoSakuhinTagList
from admin_app.dto.dto_10_sakuhin_tag.dto_21022_sakuhin_tag_create import DtoSakuhinTagCreateForm
from admin_app.dto.dto_10_sakuhin_tag.dto_21023_sakuhin_tag_update import DtoSakuhinTagUpdate

class SakuhinTagUpdateService(ServiceMain):

    # タグマスタテーブル用DAO
    dao_m_sakuhin_tag = DaoMSakuhinTag()
    dao_m_sakuhin_tag_category = DaoMSakuhinTagCategory()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self,tag_code):

        context = {}
        # 画面にタグマスタ情報を設定
        # タグコードに紐づく画面要素を取得
        param = {'tag_code':tag_code}
        tag_update_form = self.unpack(self.mapping(DtoSakuhinTagUpdate.DtoSakuhinTagUpdateData, self.dao_m_sakuhin_tag.selectUpdateData(param)))

        # タグカテゴリを取得
        dto_sakuhin_category_tag = self.mapping(DtoSakuhinTagList.DtoSakuhinTagCategoryAll, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryAll())

        if tag_update_form:
            return self.unpack({'value_not_found':False,'form':{'tag_update_form':tag_update_form[0],'sakuhin_tag_category':dto_sakuhin_category_tag}})
        else:
            return self.unpack({'value_not_found':True,'form':''})
        
        '''タグマスタ更新処理'''
    def updateSakuhinTagData(self, request):

        form = DtoSakuhinTagCreateForm(request.POST.copy())
        dto_sakuhin_category_tag = self.mapping(DtoSakuhinTagList.DtoSakuhinTagCategoryAll, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryAll())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # タグマスタの登録
            try:
                self.dao_m_sakuhin_tag.update(entity)
            except DaoMSakuhinTag.DuplicateTagNameException as e:
                # タグ名重複によりエラーの場合
                form.data['sakuhin_tag_category'] = dto_sakuhin_category_tag
                
                return self.unpack({'is_error':True,'form':{'tag_update_form':form.data,'sakuhin_tag_category':dto_sakuhin_category_tag},'insert_error_name':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin_tag','編集',form.cleaned_data['tag_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())
            
            return self.unpack({'is_error':True,'form':{'tag_update_form':form.data,'sakuhin_tag_category':dto_sakuhin_category_tag},'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にタグマスタエンティティを作成'''
    def createDtoForUpdate(self,form,full_name):
        return {
            'tag_code' : form.cleaned_data['tag_code'], # タグコード
            'tag_category_code' : form.cleaned_data['sakuhin_tag_category_code'], # タグカテゴリコード
            'tag_name' : form.cleaned_data['tag_name'], # タグ名
            'full_name' : full_name, # 作成者/更新者
            }