import json
from admin_app.service.service_main import ServiceMain

from admin_app.dao.dao_m_novel_title import DaoMNovelTitle
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_03_novel.dto_20312_novel_create import DtoNovelCreateForm
from admin_app.dto.dto_03_novel.dto_20313_novel_update import DtoNovelUpdate

class NovelUpdateService(ServiceMain):

    # 小説タイトル基本マスタテーブル用DAO
    dao_m_novel_title = DaoMNovelTitle()

    # 変更履歴
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self, novel_title_code):

        context = {}

        # 画面に小説タイトル基本マスタ情報を設定
        # 小説タイトルコードに紐づく画面要素を取得
        param = {'novel_title_code':novel_title_code}
        novel_update_form = self.unpack(self.mapping(DtoNovelUpdate.DtoNovelUpdateData, self.dao_m_novel_title.selectUpdateData(param)))

        if novel_update_form:
            return self.unpack({'value_not_found':False,'form':novel_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    '''小説タイトル基本マスタ更新処理'''
    def updateNovelData(self, request):

        # POST内容をフォームに設定
        form = DtoNovelCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # 小説タイトル基本マスタの登録
            try:
                self.dao_m_novel_title.updateNovel(entity)
                staff_entity = self.createDtoForUpdateStaff(form, full_name)
                self.dao_m_novel_title.updateStaffMap(staff_entity)
            except DaoMNovelTitle.DuplicateNovelTitleNameException as e:
                # 小説タイトル名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'update_error':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_novel_title','編集',form.cleaned_data['novel_title_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())
            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO更新用に小説タイトル基本マスタエンティティを作成'''
    def createDtoForUpdate(self,form, full_name):
        return {
                'novel_title_code' : form.cleaned_data['novel_title_code'], # 小説タイトルコード
                'novel_title_name' : form.cleaned_data['novel_title_name'], # 小説タイトル名
                'rensai_start_yyyymm' : form.data['rensai_start_yyyymm'], # 連載開始年月
                'published_cnt' : form.cleaned_data['published_cnt'], # 既刊数
                'rensai_end_flg' : form.cleaned_data['rensai_end_flg'], # 連載終了フラグ
                'award_history' : form.cleaned_data['award_history'], # 受賞歴
                'media_code' : form.cleaned_data['media_code'], # 掲載媒体コード
                'publisher_code' : form.cleaned_data['publisher_code'], # 出版社コード
                'full_name' : full_name, # 作成者/更新者
                }

    def createDtoForUpdateStaff(self,form,full_name):
        return {
            'staff_map_code' : form.cleaned_data['staff_map_code'],
            'staff_role_code1' : form.cleaned_data['staff_role_code1'],
            'staff_code1' : form.cleaned_data['staff_code1'],
            'staff_role_code2' : form.cleaned_data['staff_role_code2'],
            'staff_code2' : form.cleaned_data['staff_code2'],
            'staff_role_code3' : form.cleaned_data['staff_role_code3'],
            'staff_code3' : form.cleaned_data['staff_code3'],
            'staff_role_code4' : form.cleaned_data['staff_role_code4'],
            'staff_code4' : form.cleaned_data['staff_code4'],
            'staff_role_code5' : form.cleaned_data['staff_role_code5'],
            'staff_code5' : form.cleaned_data['staff_code5'],
            'full_name' : full_name
        }