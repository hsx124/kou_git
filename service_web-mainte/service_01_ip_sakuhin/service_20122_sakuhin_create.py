import subprocess
from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_01_ip_sakuhin.dto_20122_sakuhin_create import SakuhinCreateForm

import json

"""イメージ保存用"""
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class SakuhinCreateService(ServiceMain):

    # IPマスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def bizProcess(self):

        '''m_sakuhinに存在するIPコードの最大値を取得'''
        new_ip_code = self.dao_m_sakuhin.selectMaxIpCode()
        '''最大値+1を0埋めする（新規IPコード）'''
        new_ip_code = str(int(new_ip_code)+1).zfill(10)
            
        return self.unpack({'form':{'ip_code':new_ip_code}})

    '''IPマスタ作成処理'''
    def createMIp(self,request):

        # POST内容と受信したキービジュアルをフォームに設定
        form = SakuhinCreateForm(request.POST.copy(),request.FILES)

        # 受信した画像データよりキービジュアルファイル名の取得し、フォームに設定
        key_visual_file_name = ''
        if  'key_visual' in request.FILES:
            imgdata = request.FILES['key_visual']
            key_visual_file_name = imgdata.name
            form.data['key_visual_file_name'] = key_visual_file_name

        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()

            # 画像保存処理
            saved_thumbnail_file_name = self.saveImage(form.data['ip_code'],request,form.cleaned_data['key_visual_file_name'])

            entity = self.createDtoForInsert(form,full_name)
            # IPマスタの登録
            try : 
                self.dao_m_sakuhin.insertMIp(entity)
            except DaoMSakuhin.DuplicateIpCodeException as e:
                # IPコード重複によりエラーの場合
                ip_code = self.bizProcess()['form']['ip_code']
                form.data['ip_code'] = ip_code
                return self.unpack({'is_error':True,'form':form.data,'insert_error_ipcode':True})
            except DaoMSakuhin.DuplicateIpNameException as e:
                # IP名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_ipname':True})

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin','追加',form.cleaned_data['ip_name'],'',full_name)
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

    '''DAO登録用にIPマスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name):

        # キーワードを"/"で結合
        keyword = ''
        for i in range(15):
            tmp = form.cleaned_data['keyword'+ str(i+1)]
            if tmp == '':
                continue
            if keyword != '':
                keyword += '/'
            keyword += tmp

        return (form.cleaned_data['ip_code'], # IPコード
                form.cleaned_data['ip_name'], # IP名
                form.cleaned_data['ip_kana_name'],  # IPカナ名
                form.cleaned_data["key_visual_file_name"], # キービジュアル
                form.cleaned_data['release_date'], # 発表年月日
                form.cleaned_data['valid_start_date'], # IP公開有効期間_開始
                form.cleaned_data['valid_end_date'], # IP公開有効期間_終了
                form.cleaned_data['foreign_window'], # 国外窓口
                form.cleaned_data['domestic_window'], # 国内窓口
                form.cleaned_data['memo'], # メモ
                form.cleaned_data['overview'], # あらすじ
                form.cleaned_data['overview_wiki_title'],  # あらすじ用Wikiタイトル
                keyword, # キーワード
                full_name, # 作成者
                full_name, # 更新者
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