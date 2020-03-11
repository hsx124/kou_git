from admin_app.service.service_main import ServiceMain

from admin_app.dao.dao_m_media_report import DaoMMediaReport
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dao.dao_m_banner import DaoBanner

from admin_app.dto.dto_09_home.dto_20916_home_update import DtoHomeupdate
from admin_app.dto.dto_09_home.dto_20916_home_update import HomeUpdateForm

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import shutil

import json

class HomeUpdateService(ServiceMain):

    # m_white_paperテーブル用DAO
    dao_m_media_report = DaoMMediaReport()
    # t_change_managementテーブル用DAO
    dao_t_update_history = DaoTUpdateHistory()
    # m_bannerテーブル用DAO
    dao_m_banner = DaoBanner()

    '''初期描画'''
    def initialize(self,position):
        # 領域用DTOを画面DTOに詰める
        banner_table = self.mapping(DtoHomeupdate.DtoBanner,self.dao_m_banner.selectbanner(position))

        banner_table = banner_table[0] if banner_table else DtoHomeupdate.DtoBanner(position,'','','','',True,'','')
        media_report_table = self.mapping(DtoHomeupdate.DtoTMediaReport,self.dao_m_media_report.selectAll())
        dto_home_update = self.unpack(DtoHomeupdate(banner_table,media_report_table))
        
        # return self.unpack(dto_home_update)
        if dto_home_update['banner']['subject']:
            return self.unpack({'value_not_found':False,'dto':dto_home_update})
        else:
            return self.unpack({'value_not_found':True,'dto':''})

    '''更新プロセス'''
    def updateBannerData(self,position,title,details,external_site,media_report_code,white_paper,is_checked,request):
        # フォームの生成
        form = HomeUpdateForm(request.POST.copy(),request.FILES,initial={'is_checked':is_checked})
        if  'thumbnail' in request.FILES:
            # サムネイルファイルを受信した場合、
            # バリデーションのためにファイル名をフォームに設定
            thumbnail_file_name = ''
            imgdata = request.FILES['thumbnail']
            thumbnail_file_name = imgdata.name
            form.data['thumbnail_file_name'] = thumbnail_file_name

        if form.is_valid():
            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # 入力チェックOK
            # 画像保存処理
            saved_thumbnail_file_name = self.saveImage(position,request,form.cleaned_data['thumbnail_file_name'])
            # バナーテーブル更新
            self.dao_m_banner.updateBanner( position
                                            ,form.cleaned_data['banner_title']
                                            ,details
                                            ,saved_thumbnail_file_name
                                            ,external_site
                                            ,media_report_code
                                            ,is_checked 
                                            ,full_name)
            entity = ('m_banner','更新',title,position,full_name)

            # 変更履歴登録
            self.dao_t_update_history.insert(entity)
            return self.unpack({'is_error':False})
        else:
            # 入力チェックNG
            errors = json.loads(form.errors.as_json())
            saved_thumbnail_file_name = ''
            # 画像保存処理
            if ('thumbnail' not in errors) and ('thumbnail_file_name' not in errors):
                saved_thumbnail_file_name = self.saveImage(position,request,request.POST['thumbnail_file_name'])
            # エラー時
            banner_table = DtoHomeupdate.DtoBanner( position
                                                    ,saved_thumbnail_file_name
                                                    ,title
                                                    ,details
                                                    ,external_site
                                                    ,is_checked
                                                    ,white_paper_num
                                                    ,white_paper
                                                    )
            white_paper_table = self.mapping(DtoHomeupdate.DtoTMediaReport,self.dao_m_media_report.selectAll())
            dto_home_update = DtoHomeupdate(banner_table,white_paper_table)
            return self.unpack({'is_error':True,'errors':errors,'position':position,'dto':dto_home_update})
 
    def saveImage(self,position,request,file_name):
        if  'thumbnail' in request.FILES:
            base_url = 'image/banner/' + position +'/'
            data = request.FILES['thumbnail']
            generated_path = base_url + data.name
            actual_path = default_storage.save(generated_path, ContentFile(data.read()))
            # 同一ファイル名がすでに存在する場合、ファイル名末尾に'_'+[ランダムなアルファベット7文字]が付加される
            if not(generated_path == actual_path):
                extension = '.' + file_name.split('.')[-1]
                file_name_without_extension = file_name[0:-(len(extension))]
                return file_name_without_extension +'_'+ actual_path.split('_')[-1]
        return file_name