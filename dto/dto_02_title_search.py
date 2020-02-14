from typing import NamedTuple
from typing import List
from typing import Dict

class DtoSearchTitle(NamedTuple):
    class DtoTitleName(NamedTuple):
        prefix : str
        ip_name : str
        ip_code : str
        
    search_title : Dict[str,List[DtoTitleName]]
