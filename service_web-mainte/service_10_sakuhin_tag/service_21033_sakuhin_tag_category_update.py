import os
import json
import subprocess

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_sakuhin_tag_category import DaoMSakuhinTagCategory
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_10_sakuhin_tag.dto_21031_sakuhin_tag_category_list import DtoSakuhinTagCategoryList
from admin_app.dto.dto_10_sakuhin_tag.dto_21032_sakuhin_tag_category_create import DtoSakuhinTagCategoryCreateForm
from admin_app.dto.dto_10_sakuhin_tag.dto_21033_sakuhin_tag_category_update import DtoSakuhinTagCategoryUpdate

class SakuhinTagCategoryUpdateService(ServiceMain):

    # タグカテゴリマスタテーブル用DAO
    dao_m_sakuhin_tag_category = DaoMSakuhinTagCategory()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self,sakuhin_tag_category_code):

        context = {}
        # 画面にタグカテゴリマスタ情報を設定
        # タグカテゴリコードに紐づく画面要素を取得
        param = {'sakuhin_tag_category_code':sakuhin_tag_category_code}
        sakuhin_tag_category_update_form = self.unpack(self.mapping(DtoSakuhinTagCategoryUpdate.DtoSakuhinTagCategoryUpdateData, self.dao_m_sakuhin_tag_category.selectUpdateData(param)))

        if sakuhin_tag_category_update_form:
            return self.unpack({'value_not_found':False,'form':sakuhin_tag_category_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    '''タグカテゴリマスタ更新処理'''
    def updateSakuhinTagCategoryData(self, request):

        form = DtoSakuhinTagCategoryCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # タグカテゴリマスタの登録
            try:
                self.dao_m_sakuhin_tag_category.updateSakuhinTagCategory(entity)
            except DaoMSakuhinTagCategory.DuplicateSakuhinTagCategoryNameException as e:
                # タグカテゴリ名重複によりエラーの場合

                return self.unpack({'is_error':True,'form':form.data,'update_error':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin_tag_category','編集',form.cleaned_data['sakuhin_tag_category_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にタグカテゴリマスタエンティティを作成'''
    def createDtoForUpdate(self,form,full_name):
        return {
            'sakuhin_tag_category_code' : form.cleaned_data['sakuhin_tag_category_code'], # タグカテゴリコード
            'sakuhin_tag_category_name' : form.cleaned_data['sakuhin_tag_category_name'], # タグカテゴリ名
            'full_name' : full_name, # 作成者/更新者
            }