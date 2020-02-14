from typing import NamedTuple
from typing import List
from admin_app.dto.dto_list import DtoList

class DtoSakuhinBind(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    """作品モーダルデータ"""
    class DtoSakuhinModal(NamedTuple):
        # 作品コード
        sakuhin_code : str
        # 作品名
        sakuhin_name : str
        # 作品かな名
        sakuhin_kana_name : str
        # 更新者
        update_user: str
        # 更新日時
        update_time: str

    """関連タイトル一覧"""
    class DtoTitleList(NamedTuple):
        # マンガコード
        title_code : str
        # マンガタイトル名
        title_name : str
        # タイトルカテゴリ名
        title_category_name : str
        # タイトルカテゴリコード
        title_category_code : str
        # 更新者
        update_user: str
        # 更新日時
        update_time: str
        # 作品紐付けID
        sakuhin_map_id : str

    """関連タイトルモーダル"""
    class DtoTitleModal(NamedTuple):
        # マンガコード
        title_code : str
        # マンガタイトル名
        title_name : str
        # タイトルカテゴリ名
        title_category_name : str
        # タイトルカテゴリコード
        title_category_code : str
        # 更新者
        update_user: str
        # 更新日時
        update_time: str

    """Twitterモーダルデータ"""
    class DtoTwitterModal(NamedTuple):
        # Twitterコード
        twitter_code : str
        # ユーザ名
        user_name : str
        # アカウント名
        account_name : str
        # メインフラグ
        main_account_flg : str
        # 更新者
        update_user: str
        # 更新日時
        update_time: str

    """Twitterに関連作品モーダルデータ"""
    class DtoTwitterSakuhinModal(NamedTuple):
        # 作品コード
        sakuhin_code : str
        # 作品名
        sakuhin_name : str
        # 作品かな名
        sakuhin_kana_name : str
        # Twitterコード
        twitter_code : str
        # ユーザ名
        user_name : str
        # アカウント名
        account_name : str
        # メインフラグ
        main_account_flg : str
        # 更新者
        update_user: str
        # 更新日時
        update_time: str

    """作品一覧データ"""
    class DtoSakuhinList(NamedTuple):
        # 作品コード
        sakuhin_code : str
        # 作品名
        sakuhin_name : str
        # 作品かな名
        sakuhin_kana_name : str
        # 更新者
        update_user: str
        # 更新日時
        update_time: str
        # 作品紐付けID
        sakuhin_map_id : str

    """Twitter一覧データ"""
    class DtoTwitterList(NamedTuple):
        # Twitterコード
        twitter_code : str
        # ユーザ名
        user_name : str
        # アカウント名
        account_name : str
        # メインフラグ
        main_account_flg : str
        # 更新者
        update_user: str
        # 更新日時
        update_time: str
        # 作品紐付けID
        sakuhin_map_id : str

    """強制解除Twitterデータ"""
    class DtoDelTwitter(NamedTuple):
        # 作品紐付けID
        sakuhin_map_id : str
        # ユーザ名
        user_name : str

    """Gameモーダルデータ"""
    class DtoGamerModal(NamedTuple):
        # ゲームコード
        game_title_code : str
        # ゲーム名
        game_title_name : str
        # 販売元
        hanbai_company_name : str
        # プラットフォーム名
        platform_name : str
        # 発表年月日
        release_yyyymmdd : str
        # 更新者
        update_user: str
        # 更新日時
        update_time: str