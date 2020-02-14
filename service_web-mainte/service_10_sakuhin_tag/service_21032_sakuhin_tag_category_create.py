import os
import json
import subprocess

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_sakuhin_tag_category import DaoMSakuhinTagCategory
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_10_sakuhin_tag.dto_21031_sakuhin_tag_category_list import DtoSakuhinTagCategoryList
from admin_app.dto.dto_10_sakuhin_tag.dto_21032_sakuhin_tag_category_create import DtoSakuhinTagCategoryCreateForm

class SakuhinTagCategoryCreateService(ServiceMain):

    # タグカテゴリマスタテーブル用DAO
    dao_m_sakuhin_tag_category = DaoMSakuhinTagCategory()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self):

        # m_sakuhin_tag_categoryに存在するタグカテゴリコードの最大値を取得
        new_sakuhin_tag_category_code = self.dao_m_sakuhin_tag_category.selectMaxSakuhinTagCategoryCode()
        # 最大値+1を0埋めする（新規タグカテゴリコード）
        new_sakuhin_tag_category_code = str(int(new_sakuhin_tag_category_code)+1).zfill(5)

        # 領域用DTOを画面DTOに詰める
        return self.unpack({'form':{'sakuhin_tag_category_code':new_sakuhin_tag_category_code}})

    '''タグカテゴリマスタ作成処理'''
    def createSakuhinTagCategoryData(self,request):

        # POST内容をフォームに設定
        form = DtoSakuhinTagCategoryCreateForm(request.POST.copy())
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # Dao登録用entityを作成
            entity = self.createDtoForInsert(form,full_name)
            # タグカテゴリマスタの登録
            try :
                self.dao_m_sakuhin_tag_category.insertSakuhinTagCategory(entity)
            except DaoMSakuhinTagCategory.DuplicateSakuhinTagCategoryCodeException as e:
                # タグカテゴリコード重複によりエラーの場合
                # m_sakuhin_tag_categoryに存在するタグカテゴリコードの最大値を取得
                new_sakuhin_tag_category_code = self.dao_m_sakuhin_tag_category.selectMaxSakuhinTagCategoryCode()
                # 最大値+1を0埋めする（新規タグカテゴリコード）
                new_sakuhin_tag_category_code = str(int(new_sakuhin_tag_category_code)+1).zfill(5)
                form.data['sakuhin_tag_category_code'] = new_sakuhin_tag_category_code
                return self.unpack({'is_error':True,'form':form.data,'insert_error_sakuhin_tag_categorycode':True})

            except DaoMSakuhinTagCategory.DuplicateSakuhinTagCategoryNameException as e:
                # タグカテゴリ名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_sakuhin_tag_categoryname':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin_tag_category','追加',form.cleaned_data['sakuhin_tag_category_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})

        else :
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にタグカテゴリマスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name):
        return {
            'sakuhin_tag_category_code' : form.cleaned_data['sakuhin_tag_category_code'], # タグカテゴリコード
            'sakuhin_tag_category_name' : form.cleaned_data['sakuhin_tag_category_name'], # タグカテゴリ名
            'full_name' : full_name, # 作成者/更新者
            }