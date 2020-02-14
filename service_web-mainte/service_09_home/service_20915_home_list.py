import datetime
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_banner import DaoBanner
from admin_app.dao.dao_t_top_news import DaoNews
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_list import DtoList
from admin_app.dto.dto_09_home.dto_20915_home_list import DtoHomelist
from admin_app.dto.dto_09_home.dto_20915_home_list import NewsCreateForm

import json

class HomeListService(ServiceList):
    
    # t_change_managementテーブル用DAO
    dao_t_update_history = DaoTUpdateHistory()
    # m_bannerテーブル用DAO
    dao_m_banner = DaoBanner()
    # t_top_newsテーブル用DAO
    dao_t_top_news = DaoNews()
    
    '''初期描画'''
    def bizProcess(self,tableName,tableName2):
        # 領域用DTOを画面DTOに詰める
        # 更新履歴
        notice_table = self.getnoticetable(tableName,tableName2)
        # バナー
        banner_table = self.mapping(DtoHomelist.DtoBanner,self.dao_m_banner.selectbannerpreview())
        #お知らせ
        news = self.mapping(DtoHomelist.DtoNews, self.dao_t_top_news.selectNews())
        
        dto_home_list = DtoHomelist(notice_table,banner_table,news)
        
        return self.unpack(dto_home_list)


    '''更新プロセス'''
    def homeListProcess(self,request,id):
        form = NewsCreateForm(request.POST.copy())

        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()

            # お知らせ編集
            news_entity = self.createDtoForUpdate(form, full_name, id)
            self.dao_t_top_news.updateNews(news_entity)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('t_top_news','更新',form.cleaned_data['news_subject'],'',full_name)
            self.dao_t_update_history.insertTChangeManagement(entity)
            return self.unpack({'is_error':False})
        else:
            return self.unpack({'is_error':True,'errors':json.loads(form.errors.as_json())})

    '''新規登録プロセス'''
    def homeListCreateProcess(self,request,id):
        form = NewsCreateForm(request.POST.copy())
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()

            # お知らせ新規登録
            news_entity = self.createDtoForInsert(form, full_name)
            self.dao_t_top_news.createNews(news_entity)

            # 変更管理更新
            entity = ('t_top_news','追加',form.cleaned_data['news_subject'],'',full_name)
            self.dao_t_update_history.insertTChangeManagement(entity)
            return self.unpack({'is_error':False})
        else:
            return self.unpack({'is_error':True,'errors':json.loads(form.errors.as_json())})
    
    '''バナー非表示プロセス'''
    def homeBannerProcess(self,is_invalid,full_name):
        self.dao_m_banner.bannerDisable(is_invalid, full_name)
        status = '表示'
        if is_invalid == 'true':
            status ='非表示'
        entity = ('m_banner',status,'','',full_name)
        self.dao_t_update_history.insertTChangeManagement(entity)

    def getnoticetable(self, tableName, tableName2):

        # 更新履歴
        notice_table = self.mapping(DtoList.DtoNoticeTable, self.dao_t_update_history.selectChangeForHomeListByTableName(tableName,tableName2))

        return notice_table

    def changeCsvDownloadProcess(self, tableName, tableName2,startDate=datetime.date(1900,1,1), endDate=datetime.date(2099,12,31)):
        '''
        更新履歴CSVダウンロード処理
        '''

        csv_date = {}
        csv_date = self.dao_t_update_history.selectChangeRecordForHomeListByDate(tableName,tableName2,startDate,endDate)

        return csv_date


    def createDtoForInsert(self, form, full_name):
        '''
        お知らせ新規登録用エンティティを作成
        '''
        return (
                form.cleaned_data['news_subject'],
                form.cleaned_data['news_headline'],
                form.cleaned_data['news_info_detail'],
                form.cleaned_data['news_link_url'],
                full_name
                )

    def createDtoForUpdate(self, form, full_name, id):
        '''
        お知らせ編集用エンティティを作成
        '''
        return (
                form.cleaned_data['news_subject'],
                form.cleaned_data['news_headline'],
                form.cleaned_data['news_info_detail'],
                form.cleaned_data['news_link_url'],
                full_name,
                id,
                )