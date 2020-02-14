from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoIpBind(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    class DtoIpBindList(NamedTuple):
        """IPマスタ一覧"""
        class DtoIpData(NamedTuple):
            # IPコード
            ip_code : str
            # IP名
            ip_name : str
            #IPかな名
            ip_kana_name : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str

        """関連作品一覧"""
        class DtoConnectionSakuhin(NamedTuple):
            # 作品コード
            sakuhin_code : str
            # 作品名
            sakuhin_name : str
            #作品かな名
            sakuhin_kana_name : str
            # IP紐付け更新者
            update_user: str
            # IP紐付け更新日時
            update_time: str
            # IP紐付けID
            ip_map_id: str

        """関連作品一覧（モーダル）"""
        class DtoConnectionSakuhinModal(NamedTuple):
            # 作品コード
            sakuhin_code : str
            # 作品名
            sakuhin_name : str
            #作品かな名
            sakuhin_kana_name : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str

        """関連IP一覧"""
        class DtoConnectionIpData(NamedTuple):
            # 作品コード
            ip_code : str
            # 作品名
            ip_name : str
            #作品かな名
            ip_kana_name : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str
            # IP紐付けID
            ip_map_id: str