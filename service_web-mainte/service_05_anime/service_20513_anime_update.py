import json
import re
from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_m_anime_title import DaoMAnimeTitle
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_list import DtoList
from admin_app.dto.dto_05_anime.dto_20512_anime_create import AnimeCreateForm
from admin_app.service.service_main import ServiceMain
from admin_app.dto.dto_05_anime.dto_20513_anime_update import DtoAnimeUpdate

class AnimeUpdateService(ServiceMain):

    # IPマスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()

    # アニメタイトル基本マスタテーブル用DAO
    dao_m_anime_title = DaoMAnimeTitle()

    # 変更履歴
    dao_t_update_history = DaoTUpdateHistory()

    def bizProcess(self, ipcode, animename):
        '''
        初期描画
        '''

        entity = (ipcode, animename)

        # IPコードからIPを検索
        anime_update_form = self.unpack(self.mapping(DtoAnimeUpdate.DtoAnimeUpdateData, self.dao_m_wiki.selectMWikiByIpCodeAnimeName(entity)))
        
        # BRタグを改行コードに置き換える
        tmp = anime_update_form[0]
        if (tmp):
            tmp['broadcaster'] = re.sub('<br ?/?>','\r\n', tmp['broadcaster'])
            tmp['period'] = re.sub('<br ?/?>','\r\n', tmp['period'])

        return self.unpack({'form':tmp})

    def updateMWiki(self, request, animename):
        '''
        wikiマスタ（アニメマスタ）更新
        '''

        # POST内容と受信したキービジュアルをフォームに設定
        form = AnimeCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():
            # 入力チェックOK
            # ユーザの姓名取得
            full_name = request.user.get_full_name()

            # データ取得
            entity = self.createDtoForUpdate(form, full_name, animename)

            # wikiマスタ（アニメマスタ）の登録
            self.dao_m_wiki.updateMWiki(entity)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_wiki','編集',form.cleaned_data['tv_program_name'],'',full_name)
            self.dao_t_update_history.insertTChangeManagement(entity)

            return self.unpack({'is_error':False})
        else :
            # 入力チェックNG

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    def createDtoForUpdate(self, form, full_name, animename):
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

        return (form.cleaned_data['tv_program_name'],  # TV番組名
                broadcaster, # 放送局
                period, # 放送期間
                full_name, # 更新者

                form.cleaned_data['ip_code'],  # IPコード（レコード特定用）
                animename # TV番組名（レコード特定用）
                )