import json
from admin_app.service.service_main import ServiceMain

from admin_app.dao.dao_m_twitter import DaoMTwitter
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_07_twitter.dto_20712_twitter_create import DtoTwitterCreateForm
from admin_app.dto.dto_07_twitter.dto_20713_twitter_update import DtoTwitterUpdate
from admin_app.dao.dao_m_sakuhin_map import DaoMSakuhinMap

class TwitterUpdateService(ServiceMain):
    # 作品紐付けマスタテーブル用DAO
    dao_m_sakuhin_map = DaoMSakuhinMap()
    # ツイッターマスタテーブル用DAO
    dao_m_twitter = DaoMTwitter()
    # 更新履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self, twitter_code):

        context = {}

        # 画面に掲載媒体マスタ情報を設定
        # 掲載媒体コードに紐づく画面要素を取得
        param = {'twitter_code':twitter_code}
        twitter_update_form = self.unpack(self.mapping(DtoTwitterUpdate.UpdateData, self.dao_m_twitter.selectUpdateData(param)))

        if twitter_update_form:
            return self.unpack({'value_not_found':False,'form':twitter_update_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    def changeMainFlg(self,param):
        change_mainflg_form = self.unpack(self.mapping(DtoTwitterUpdate.BindData,self.dao_m_twitter.selectMapSakuhinByTwitterCode(param)))
        if len(change_mainflg_form) == 0 :
            return None
        return change_mainflg_form[0]

    def deleteMapData(self,param):
        # 削除する前に当該データの無効フラグを確認
        invalid_flg =  self.dao_m_twitter.selectInvalidFlg(param)
        
        #削除フラグ（当削除対象が既に削除したかフラグ）
        delflg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delflg = True
        else:
            # sakuhin_map_idに合致するレコードを論理削除

            # 作品紐付け解除処理を行う
            self.dao_m_sakuhin_map.updateInvalidFlgBy(param)
             # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin_map', '紐づけ解除', param['account_name'], '', param['full_name'])
            self.dao_t_update_history.insert(entity)
        return self.unpack({'is_error':delflg})
    '''掲載媒体マスタ更新処理'''
    def updateTwitterData(self, request):
        
        # POST内容と受信したキービジュアルをフォームに設定
        form = DtoTwitterCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            entity = self.createDtoForUpdate(form, full_name)

            # 掲載媒体マスタの登録
            try:
                self.dao_m_twitter.update(entity)
            except DaoMTwitter.DuplicateUserNameException as e:
                # ユーザー名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_username':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_twitter','編集',form.cleaned_data['account_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})
        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にTwitterマスタエンティティを作成'''
    def createDtoForUpdate(self,form,full_name):
        return {
            'twitter_code' : form.cleaned_data['twitter_code'], # Twitterコード
            'account_name' : form.cleaned_data['account_name'], # アカウント名
            'user_name' : form.cleaned_data['user_name'], # ユーザー名
            'main_account_flg' : form.cleaned_data['main_account_flg'], # メインアカウントフラグ
            'full_name' : full_name, # 更新者
            }