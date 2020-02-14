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

class SakuhinTagCreateService(ServiceMain):

    # タグマスタテーブル用DAO
    dao_m_sakuhin_tag = DaoMSakuhinTag()
    dao_m_sakuhin_tag_category = DaoMSakuhinTagCategory()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self):

        # m_sakuhin_tagに存在するタグコードの最大値を取得
        new_tag_code = self.dao_m_sakuhin_tag.selectMaxTagCode()
        # 最大値+1を0埋めする（新規タグコード）
        new_tag_code = str(int(new_tag_code)+1).zfill(10)
        # タグカテゴリを取得
        dto_sakuhin_category_tag = self.mapping(DtoSakuhinTagList.DtoSakuhinTagCategoryAll, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryAll())
        # 領域用DTOを画面DTOに詰める
        return self.unpack({'form':{'tag_code':new_tag_code,'sakuhin_tag_category':dto_sakuhin_category_tag}})
        
    '''タグマスタ作成処理'''
    def createSakuhinTagData(self,request):

        # POST内容をフォームに設定
        form = DtoSakuhinTagCreateForm(request.POST.copy())
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # Dao登録用entityを作成
            entity = self.createDtoForInsert(form,full_name)
            # タグマスタの登録
            try : 
                self.dao_m_sakuhin_tag.insert(entity)
            except DaoMSakuhinTag.DuplicateTagCodeException as e:
                # タグコード重複によりエラーの場合
                # m_sakuhin_tagに存在するタグコードの最大値を取得
                new_tag_code = self.dao_m_sakuhin_tag.selectMaxTagCode()
                # 最大値+1を0埋めする（新規タグコード）
                max_code = str(int(new_tag_code)+1).zfill(10)
                form.data['tag_code'] = max_code
                return self.unpack({'is_error':True,'form':form.data,'insert_error_tagcode':True})

            except DaoMSakuhinTag.DuplicateTagNameException as e:
                dto_sakuhin_category_tag = self.mapping(DtoSakuhinTagList.DtoSakuhinTagCategoryAll, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryAll())
                form.data['sakuhin_tag_category'] = dto_sakuhin_category_tag
                # タグ名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_tagname':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin_tag','追加',form.cleaned_data['tag_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})

        else :
            dto_sakuhin_category_tag = self.mapping(DtoSakuhinTagList.DtoSakuhinTagCategoryAll, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryAll())
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())
            form.data['sakuhin_tag_category'] = dto_sakuhin_category_tag

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にタグマスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name):
        return {
            'tag_code' : form.cleaned_data['tag_code'], # タグコード
            'tag_category_code' : form.cleaned_data['sakuhin_tag_category_code'], # タグカテゴリコード
            'tag_name' : form.cleaned_data['tag_name'], # タグ名
            'full_name' : full_name, # 作成者/更新者
            }