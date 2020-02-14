import os
import json
import subprocess

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from admin_app.service.service_main import ServiceMain
from admin_app.dao.dao_m_ip import DaoMIp
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_01_ip_sakuhin.dto_20112_ip_create import DtoIpCreateForm

class IpCreateService(ServiceMain):

    # IPマスタテーブル用DAO
    dao_m_ip = DaoMIp()
    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self):

        # m_ipに存在するIPコードの最大値を取得
        new_code = self.dao_m_ip.selectMaxIpCode()
        # 最大値+1を0埋めする（新規IPコード）
        max_code = 'IP'+str(int(new_code[2:])+1).zfill(8)
            
        return self.unpack({'form':{'ip_code':max_code}})

    '''IPマスタ作成処理'''
    def createIpData(self,request):

        # POST内容をフォームに設定
        form = DtoIpCreateForm(request.POST.copy())
        
        # 入力チェック
        if form.is_valid():
            # 入力チェックOK

            # ユーザの姓名取得
            full_name = request.user.get_full_name()
            # Dao登録用entityを作成
            entity = self.createDtoForInsert(form,full_name)

            # IPマスタの登録
            try : 
                self.dao_m_ip.insert(entity)
            except DaoMIp.DuplicateIpCodeException as e:
                # IPコード重複によりエラーの場合

                # m_ipに存在するIPコードの最大値を取得
                new_code = self.dao_m_ip.selectMaxIpCode()
                # 最大値+1を0埋めする（新規IPコード）
                max_code = 'IP'+str(int(new_code[2:])+1).zfill(8)

                form.data['ip_code'] = max_code
                return self.unpack({'is_error':True,'form':form.data,'insert_error_code':True})

            except DaoMIp.DuplicateIpNameException as e:
                # IP名重複によりエラーの場合
                return self.unpack({'is_error':True,'form':form.data,'insert_error_name':True})

            # 更新履歴の登録
            # (更新テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_ip','追加',form.cleaned_data['ip_name'],'',full_name)
            self.dao_t_update_history.insert(entity)

            return self.unpack({'is_error':False})

        else :
           # 入力チェックNG
            errors = json.loads(form.errors.as_json())

            return self.unpack({'is_error':True,'form':form.data,'errors':json.loads(form.errors.as_json())})

    '''DAO登録用にIPマスタエンティティを作成'''
    def createDtoForInsert(self,form,full_name):
        return {
            'ip_code' : form.cleaned_data['ip_code'], # IPコード
            'ip_name' : form.cleaned_data['ip_name'], # IP名
            'ip_kana_name' : form.cleaned_data['ip_kana_name'], # IPかな名
            'ip_control_flg' : form.cleaned_data['ip_control_flg'], # IP管理フラグ
            'full_name' : full_name, # 作成者/更新者
            }