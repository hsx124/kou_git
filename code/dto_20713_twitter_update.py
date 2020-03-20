from typing import NamedTuple

class DtoTwitterUpdate(NamedTuple):

    '''Twitter 編集画面連携用'''
    class UpdateData(NamedTuple):
        twitter_code : str # ツイッターコード
        account_name : str # アカウント名
        user_name : str # ユーザー名
        main_account_flg : str # メインアカウントフラグ

    class BindData(NamedTuple):
        sakuhin_map_id : str
        twitter_code : str
        account_name : str
        user_name : str
