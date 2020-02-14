from typing import NamedTuple
from typing import List
from typing import Dict

class DtoLinkCollection(NamedTuple):
    # リンクDto（1リンク）
    class DtoLink(NamedTuple):
        # 白書.ID
        id : str
        # 白書.ファイル名
        file_name : str
        # 白書.白書カテゴリ
        whitepaper_category : str
        # 白書.内容説明
        instructions : str
        # 白書.年度
        year : str
        
    # 辞書{キー（年度）: 辞書{キー（カテゴリ）:リンクDto（1リンク）}}
    link_collection : Dict[str,Dict[str,List[DtoLink]]]
