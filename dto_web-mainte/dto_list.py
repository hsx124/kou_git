from typing import NamedTuple
from typing import List

class DtoList(NamedTuple):

    class DtoNoticeTable(NamedTuple):
        '''
        更新履歴
        '''
        # 更新日時
        update_date : str
        # 更新者
        update_user : str
        # 更新テーブル
        update_table : str
        # 更新対象
        target_name : str
        # 操作内容
        operation : str
        # 備考
        remarks : str
    class DtoSakuhinSearchResult(NamedTuple):
        '''
        IPコード検索結果
        '''
        sakuhin_code : str
        sakuhin_name : str
    class DtoUpdateHistoryCsv(NamedTuple):
        '''
        更新履歴CSV出力用
        '''
        # 更新日時
        update_date : str
        # 更新者
        update_user : str
        # 更新テーブル
        update_table : str
        # 更新対象
        target_name : str
        # 操作内容
        operation : str
        # 備考
        remarks : str

    update_history_csv : List[DtoUpdateHistoryCsv]
