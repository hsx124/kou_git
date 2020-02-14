import subprocess
from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_01_ip_sakuhin.dto_20123_sakuhin_update import DtoSakuhinUpdate
from admin_app.dto.dto_01_ip_sakuhin.dto_20122_sakuhin_create import SakuhinCreateForm

import json

"""イメージ保存用"""
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class SakuhinUpdateService(ServiceMain):

    # IPマスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()

    # 変更履歴
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self, sakuhincode):

        context = {}

        # 画面にIPマスタ情報を設定
        # IPコードに紐づく画面要素を取得
        sakuhin_update_form =self.unpack(self.mapping(DtoSakuhinUpdate.DtoSakuhinUpdateDate, self.dao_m_sakuhin.selectSakuhinUpdateDataBySakuhinCode(sakuhincode)))

        # 画面フォームに表示
        # キーワードの分割
        if None != sakuhin_update_form[0]['keyword']:
            keyword = sakuhin_update_form[0]['keyword']
            keywords = keyword.split('/')
            for i, val in enumerate(keywords):
                sakuhin_update_form[0]['keyword'+ str(i+1)] = val

        return self.unpack({'form':sakuhin_update_form[0]})

    def updateMIp(self, request):
        '''
        IPマスタ更新処理
        '''
        # POST内容と受信したキービジュアルをフォームに設定
        form = SakuhinCreateForm(request.POST.copy(),request.FILES)
        # 受信した画像データよりキービジュアルファイル名を取得し、フォームに設定
        if  'key_visual' in request.FILES:
            key_visual_file_name = ''
            imgdata = request.FILES['key_visual']
            key_visual_file_name = imgdata.name
            form.data['key_visual_file_name'] = key_visual_file_name

        # 入力チェック
        if form.is_valid():

            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()

            # 画像保存処理
            saved_thumbnail_file_name = self.saveImage(form.data['ip_code'], request, form.cleaned_data['key_visual_file_name'])

            entity = self.createDtoForUpdate(form, saved_thumbnail_file_name, full_name)
            # IPマスタの登録
            try:
                self.dao_m_sakuhin.updateMIp(entity)
            except DaoMSakuhin.DuplicateIpNameException as e:
                # IP名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin','編集',form.cleaned_data['ip_name'],'',full_name)
            self.dao_t_update_history.insertTChangeManagement(entity)

            return self.unpack({'is_error':False})
        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())
            saved_thumbnail_file_name = ''
            # 画像保存処理
            if ('key_visual' not in errors) and ('key_visual_file_name' not in errors):
                saved_thumbnail_file_name = self.saveImage(form.data['ip_code'], request, form.cleaned_data['key_visual_file_name'])

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    def createDtoForUpdate(self,form, thumbnailName, full_name):
        '''
        DAO更新用にIPマスタエンティティを作成
        '''

        # キーワードを"/"で結合
        keyword = ''
        for i in range(15):
            tmp = form.cleaned_data['keyword'+ str(i+1)]
            if tmp == '':
                continue
            if keyword != '':
                keyword += '/'
            keyword += tmp

        return (
                form.cleaned_data['ip_name'], # IP名
                form.cleaned_data['ip_kana_name'],  # IPカナ名
                thumbnailName, # キービジュアル
                form.cleaned_data['release_date'], # 発表年月日
                form.cleaned_data['valid_start_date'], # IP公開有効期間_開始
                form.cleaned_data['valid_end_date'], # IP公開有効期間_終了
                form.cleaned_data['foreign_window'], # 国外窓口
                form.cleaned_data['domestic_window'], # 国内窓口
                form.cleaned_data['memo'], # メモ
                form.cleaned_data['overview'], # あらすじ
                form.cleaned_data['overview_wiki_title'],  # あらすじ用Wikiタイトル
                keyword, # キーワード
                full_name, # 更新者
                form.cleaned_data['ip_code'] # IPコード
                )

    def saveImage(self, ipcode, request, file_name):
        if  'key_visual' in request.FILES:
            base_url = 'image/keyvisual/' + ipcode +'/'
            data = request.FILES['key_visual']
            generated_path = base_url + data.name
            actual_path = default_storage.save(generated_path, ContentFile(data.read()))
            # 同一ファイル名がすでに存在する場合、ファイル名末尾に'_'+[ランダムなアルファベット7文字]が付加される
            if not(generated_path == actual_path):
                extension = '.' + file_name.split('.')[-1]
                file_name_without_extension = file_name[0:-(len(extension))]
                return file_name_without_extension +'_'+ actual_path.split('_')[-1]
        return file_name