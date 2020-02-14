from typing import NamedTuple
from typing import List
from typing import Dict

class DtoSimilarSearch(NamedTuple):
    class DtoCore(NamedTuple):
        core_code :str
        core_name : str  

    class DtoMedia(NamedTuple):
        media_code :str
        media_name : str

    class DtoImp(NamedTuple):
        imp_code :str
        imp_name : str

    class DtoFactTag(NamedTuple):
        fact_tag_category_name : str
        fact_tag_code :str
        fact_tag_name : str

    core : List[DtoCore]
    media : List[DtoMedia]
    imp : List[List[DtoImp]]
    fact_tag : Dict[str,List[DtoFactTag]]
