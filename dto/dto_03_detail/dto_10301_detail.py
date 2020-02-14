from typing import NamedTuple
from typing import List

class DtoDetail(NamedTuple):
    class DtoSakuhinData(NamedTuple):

        keyvisual_file_name : str
        sakuhin_code : str
        sakuhin_name : str
        sakuhin_kana_name : str
        overview : str
        release_yyyymm : str
        update_time : str
        foreign_window : str
        domestic_window : str
        memo : str

    sakuhin_data : DtoSakuhinData