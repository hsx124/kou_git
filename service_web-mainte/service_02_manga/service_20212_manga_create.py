import json
from admin_app.dao.dao_m_manga_title import DaoMMangaTitle
from admin_app.dao.dao_m_media import DaoMMedia
from admin_app.dao.dao_m_publisher import DaoMPublisher
from admin_app.dao.dao_m_staff_map import DaoMStaffMap
from admin_app.dao.dao_m_staff_role import DaoMStaffRole
from admin_app.dao.dao_m_staff import DaoMStaff
from admin_app.service.service_main import ServiceMain

from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_list import DtoList
from admin_app.dto.dto_02_manga.dto_20212_manga_create import DtoMangaCreateForm

class MangaCreateService(ServiceMain):

    # テーブル用DAO
    dao_m_manga_title = DaoMMangaTitle()
    dao_m_media = DaoMMedia()
    dao_m_publisher = DaoMPublisher()
    dao_m_staff_map = DaoMStaffMap()
    dao_m_staff_role = DaoMStaffRole()
    dao_m_staff = DaoMStaff()

    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self):

        # m_mangaに存在するマンガタイトルコードの最大値を取得
        new_manga_title_code = self.dao_m_manga_title.selectMaxMangaTitleCode()
        # 最大値+1を0埋めする（新規マンガタイトルコード）
        new_manga_title_code = 'M' + str(int(new_manga_title_code[1:])+1).zfill(9)

        return self.unpack({'form':{'manga_title_code': new_manga_title_code}})

    '''マンガタイトル基本マスタ作成処理'''
    def createMangaData(self,request):

        # POST内容をフォームに設定
        form = DtoMangaCreateForm(request.POST.copy())
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # m_mangaに存在するスタッフ紐づけコードの最大値を取得
            new_staff_map_code = self.dao_m_staff_map.selectMaxStaffMapCode()
            new_staff_map_code = str(int(new_staff_map_code)+1).zfill(10)
            # Dao登録用entityを作成
            entity = self.createDtoForInsert(form,full_name,new_staff_map_code)

            # マンガタイトル基本マスタの登録
            try :
                self.dao_m_manga_title.insertManga(entity)
                # 取得しておいたスタッフ紐づけコードの最大値でスタッフ紐づけマスタに新規登録をする
                staff_entity = self.createDtoForInsertStaff(form,full_name,new_staff_map_code)
                self.dao_m_manga_title.insertStaffMap(staff_entity)
            except DaoMMangaTitle.DuplicateMangaTitleCodeException as e:
                # マンガタイトルコード重複によりエラーの場合
                # 新規番号を再発行しformに返す
                new_manga_title_code = self.dao_m_manga_title.selectMaxMangaTitleCode()
                new_manga_title_code = 'M' + str(int(new_manga_title_code[1:])+1).zfill(9)
                form.data['manga_title_code'] = new_manga_title_code

                return self.unpack({'is_error':True,'form':form.data,'insert_error_mangacode':True})

            except DaoMMangaTitle.DuplicateMangaTitleNameException as e:
                # マンガタイトル名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_manganame':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_manga_title','追加',form.cleaned_data['manga_title_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})

        else :
        # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':errors})

    '''DAO登録用にマンガタイトル基本マスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name,staff_map_code):
        return {
            'manga_title_code' : form.cleaned_data['manga_title_code'], # マンガタイトルコード
            'manga_title_name' : form.cleaned_data['manga_title_name'], # マンガタイトル名
            'rensai_start_yyyymm' : form.data['rensai_start_yyyymm'], # 連載開始年月
            'published_cnt' : form.cleaned_data['published_cnt'], # 既刊数
            'rensai_end_flg' : form.cleaned_data['rensai_end_flg'], # 連載終了フラグ
            'award_history' : form.cleaned_data['award_history'], # 受賞歴
            'media_code' : form.cleaned_data['media_code'], # 掲載媒体コード
            'publisher_code' : form.cleaned_data['publisher_code'], # 出版社コード
            'staff_map_code' : staff_map_code, # スタッフ紐づけコード
            'full_name' : full_name, # 作成者/更新者
            }

    def createDtoForInsertStaff(self,form,full_name,staff_map_code):
        return {
            'staff_map_code' : staff_map_code,
            'title_category_code' : '01',
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

    def searchMedia(self,keyword):
        if len(keyword) == 0:
            # キーワードが何も入力されていないで検索された場合全件検索
            media = self.mapping(DtoMangaCreateForm.DtoMedia,self.dao_m_media.selectMediaByBook())
        else:
            # 入力された場合はあいまい検索
            media = self.mapping(DtoMangaCreateForm.DtoMedia,self.dao_m_media.selectMediaKeyword(keyword))

        # 検索結果を画面に返す
        return media

    def searchPublisher(self,keyword):
        if len(keyword) == 0:
            # キーワードが何も入力されていないで検索された場合全件検索
            publisher = self.mapping(DtoMangaCreateForm.DtoPublisher,self.dao_m_publisher.selectPublisherByBook())
        else:
            # 入力された場合はあいまい検索
            publisher = self.mapping(DtoMangaCreateForm.DtoPublisher,self.dao_m_publisher.selectPublisherKeyword(keyword))

        # 検索結果を画面に返す
        return publisher

    def searchStaffRole(self,keyword):
        if len(keyword) == 0:
            # キーワードが何も入力されていないで検索された場合全件検索
            role = self.mapping(DtoMangaCreateForm.DtoStaffRole,self.dao_m_staff_role.selectStaffRoleByBook())
        else:
            # 入力された場合はあいまい検索
            role = self.mapping(DtoMangaCreateForm.DtoStaffRole,self.dao_m_staff_role.selectStaffRoleKeyword(keyword))

        # 検索結果を画面に返す
        return role

    def searchStaff(self,keyword):
        if len(keyword) == 0:
            # キーワードが何も入力されていないで検索された場合全件検索
            staff = self.mapping(DtoMangaCreateForm.DtoStaff,self.dao_m_staff.selectStaffByBook())
        else:
            # 入力された場合はあいまい検索
            staff = self.mapping(DtoMangaCreateForm.DtoStaff,self.dao_m_staff.selectStaffKeyword(keyword))

        # 検索結果を画面に返す
        return staff