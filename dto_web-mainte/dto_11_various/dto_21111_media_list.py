from typing import NamedTuple
from typing import List

from admin_app.dto.dto_list import DtoList

class DtoMediaList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    class DtoMediaMasterList(NamedTuple):
        """掲載媒体マスタ一覧"""
        class DtoMediaMasterListData(NamedTuple):
            # 掲載媒体コード
            media_code : str
            # 掲載媒体名
            media_name : str
            # 表示フラグ
            show_flg : str
            # 優先順位
            priority : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str

        """掲載媒体マスタ一覧(CSV用)"""
        class DtoMediaMasterListForCSV(NamedTuple):
            # 掲載媒体コード
            media_code : str
            # 掲載媒体名
            media_name : str
            # 表示フラグ
            show_flg : str
            # 優先順位
            priority : str
            # 作成者
            create_user : str
            # 作成日時
            create_time : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str