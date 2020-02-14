from typing import NamedTuple
from typing import List
from typing import Dict

class DtoSearchAge(NamedTuple):
    class DtoAgeName(NamedTuple):
        release_date : str
        ip_name : str
        ip_code : str
        
    search_age : Dict[str,List[DtoAgeName]]