from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoMangaSeinendaiList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    class DtoMangaSeinendaiMasterList(NamedTuple):
        """性年代マスタ一覧"""
        class DtoMangaSeinendaiMasterListData(NamedTuple):
            # 性年代コード
            seinendai_code : str
            # マンガタイトルコード
            manga_title_code : str
            # マンガタイトル名
            manga_title_name : str
            # 総人数
            total_cnt : str
            # 男性総人数
            male_cnt : str
            # 女性総人数
            female_cnt : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str

        """性年代マスタ一覧(CSV用)"""
        class DtoMangaSeinendaiMasterListForCSV(NamedTuple):
            # マンガタイトルコード
            manga_title_code : str
            # マンガタイトル名
            manga_title_name : str
            # 総人数
            total_cnt : str
            # 男性総人数
            male_cnt : str
            # 女性総人数
            female_cnt : str
            # 作成者
            create_user : str
            # 作成日時
            create_time : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str