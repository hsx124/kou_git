import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_media import DaoMMedia
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_11_various.dto_21112_media_create import DtoMediaCreateForm

class MediaCreateService(ServiceMain):

    # 掲載媒体マスタテーブル用DAO
    dao_m_media = DaoMMedia()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self):

        # m_mediaに存在する掲載媒体コードの最大値を取得
        new_media_code = self.dao_m_media.selectMaxMediaCode()
        # 最大値+1を0埋めする（新規掲載媒体コード）
        new_media_code = str(int(new_media_code)+1).zfill(5)
            
        return self.unpack({'form':{'media_code':new_media_code}})

    '''掲載媒体マスタ作成処理'''
    def createMediaData(self,request):

        # POST内容をフォームに設定
        form = DtoMediaCreateForm(request.POST.copy())
        
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # Dao登録用entityを作成
            entity = self.createDtoForInsert(form,full_name)

            # 掲載媒体マスタの登録
            try : 
                self.dao_m_media.insert(entity)
            except DaoMMedia.DuplicateMediaCodeException as e:
                # 掲載媒体コード重複によりエラーの場合

                # m_mediaに存在する掲載媒体コードの最大値を取得
                new_code = self.dao_m_media.selectMaxMediaCode()
                # 最大値+1を0埋めする（新規掲載媒体コード）
                max_code = str(int(new_code)+1).zfill(5)

                form.data['media_code'] = max_code
                return self.unpack({'is_error':True,'form':form.data,'insert_error_mediacode':True})

            except DaoMMedia.DuplicateMediaNameException as e:
                # 掲載媒体名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_medianame':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_media','追加',form.cleaned_data['media_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})

        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用に掲載媒体マスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name):
        return {
            'media_code' : form.cleaned_data['media_code'], # 掲載媒体コード
            'media_name' : form.cleaned_data['media_name'], # 掲載媒体名
            'show_flg' : form.cleaned_data['show_flg'], # 表示/非表示
            'priority' : form.cleaned_data['priority'], # 優先順位
            'full_name' : full_name, # 作成者/更新者
            }