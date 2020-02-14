from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoAppList(NamedTuple):

    class DtoAppMasterList(NamedTuple):
        '''
        アプリマスタ一覧表示用
        '''
        ip_code : str
        app_name : str
        app_id_ios : str
        app_id_android: str
        distributor_name: str
        start_date : str
        end_date : str
        update_user : str
        update_date : str

    notice_table : DtoList.DtoNoticeTable
    app_master_list : DtoAppMasterList
