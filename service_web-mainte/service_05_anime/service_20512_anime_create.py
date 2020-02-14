import json
import re
from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_m_anime_title import DaoMAnimeTitle
from admin_app.dao.dao_t_update_history  import DaoTUpdateHistory

from admin_app.dto.dto_list import DtoList
from admin_app.dto.dto_05_anime.dto_20512_anime_create import AnimeCreateForm

from admin_app.service.service_main import ServiceMain

class AnimeCreateService(ServiceMain):

    # IPマスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()

    # アニメタイトル基本マスタテーブル用DAO
    dao_m_anime_title = DaoMAnimeTitle()

    # 変更履歴
    dao_t_update_history = DaoTUpdateHistory()

    def bizProcess(self, ipcode):
        '''
        初期描画
        '''

        # IPコードからIPを検索
        ip_search_result = self.unpack(self.mapping(DtoList.DtoIpSearchResult, self.dao_m_sakuhin.selectIpMasterByIpCode(ipcode)))

        # アニメ重複チェック
        try:
            if(0 < self.dao_m_wiki.selectCountAnimeByIpCode(ipcode)):
                raise self.dao_m_wiki.DuplicateAnimeException
        except DaoMWiki.DuplicateAnimeException as e:
            return self.unpack({'is_error':True,'create_error_anime':True,'form':ip_search_result[0]})


        return self.unpack({'form':{'ip_code':ipcode, 'ip_name':ip_search_result[0]['ip_name']}})

    def createMWiki(self, request):
        '''
        アニメマスタ新規登録
        '''
        # POST内容と受信したキービジュアルをフォームに設定
        form = AnimeCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
        
            entity = self.createDtoForInsert(form, full_name)

            # アニメマスタ編集
            try:
                self.dao_m_wiki.insertMWiki(entity)
            # アニメ登録済み
            except DaoMWiki.DuplicateAnimeException as e:
                return self.unpack({'is_error':True,'form':form.data,'insert_error_anime':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_wiki','追加',form.cleaned_data['tv_program_name'],'',full_name)
            self.dao_t_update_history.insertTChangeManagement(entity)
            return self.unpack({'is_error':False})
        else :
            # 入力チェックNG

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    def createDtoForInsert(self,form,full_name):
        '''
        DAO登録用にアニメマスタエンティティを作成
        '''

        # テキストエリア内の改行コードをBRタグに置換
        period = ''
        if(form.cleaned_data['period']):
            tmp = form.cleaned_data['period']
            period = re.sub('\r\n|\n|\r', '<br/>', tmp)

        broadcaster = ''
        if(form.cleaned_data['broadcaster']):
            tmp = form.cleaned_data['broadcaster']
            broadcaster = re.sub('\r\n|\n|\r', '<br/>', tmp)

        return (form.cleaned_data['ip_code'], # IPコード
                form.cleaned_data['tv_program_name'],  # TV番組名
                broadcaster, # 放送局
                period, # 放送期間

                full_name, # 作成者
                full_name, # 更新者
                )